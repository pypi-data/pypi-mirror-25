import math
import time
import unittest

import six

import run_lambda.call as call_module
import run_lambda.context as context_module
import run_lambda.utils as utils
import tests.square_root as square_root


class RunLambdaTest(unittest.TestCase):

    def test_utils(self):
        for length in range(10):
            hex_string = utils.random_hex(length)
            self.assertIsInstance(hex_string, str)
            self.assertEqual(len(hex_string), length)
            for character in hex_string:
                self.assertIn(character, "0123456789abcdef")
        for _ in range(10):
            request_id = utils.random_aws_request_id()
            self.assertIsInstance(request_id, str)
            self.assertGreater(len(request_id), 0)
        for _ in range(10):
            stream_name = utils.random_log_stream_name("$LATEST")
            self.assertIsInstance(stream_name, str)
            self.assertGreater(len(stream_name), 0)

    def test_context1(self):
        context = context_module.MockLambdaContext.Builder()\
            .set_function_name("test_function_name")\
            .set_function_version("version_1.0")\
            .set_memory_limit_in_mb("1000")\
            .set_log_group_name("test_log_group_name")\
            .set_default_remaining_time_in_millis(100)\
            .build()
        self.assertEqual(context.function_name, "test_function_name")
        self.assertEqual(context.function_version, "version_1.0")
        self.assertIsInstance(context.invoked_function_arn, str)
        self.assertEqual(context.memory_limit_in_mb, "1000")
        self.assertIsInstance(context.aws_request_id, str)
        self.assertEqual(context.log_group_name, "test_log_group_name")
        self.assertIsInstance(context.log_stream_name, str)
        self.assertIsNone(context.identity)
        self.assertIsNone(context.client_context)
        self.assertEqual(context.get_remaining_time_in_millis(), 100)

    def test_context2(self):
        context = context_module.MockLambdaContext.Builder()\
            .set_invoked_function_arn("invoked_function_arn")\
            .set_aws_request_id("aws_request_id")\
            .set_log_stream_name("log_stream_name")\
            .set_identity(context_module.MockCognitoIdentity(
                identity_id="identity_id",
                identity_pool_id="identity_pool_id"
            ))\
            .set_client_context(context_module.MockClientContext(
                client=context_module.MockClientContext.Client(
                    installation_id="installation_id",
                    app_title="app_title",
                    app_version_name="app_version_name",
                    app_version_code="app_version_code",
                    app_package_name="app_package_name"),
                custom={"custom_key": "custom_value"},
                env={"env_key": "env_value"}
            ))\
            .build()

        self.assertIsInstance(context.function_name, str)
        self.assertEqual(context.function_version, "$LATEST")
        self.assertEqual(context.invoked_function_arn, "invoked_function_arn")
        self.assertIsInstance(context.memory_limit_in_mb, str)
        self.assertEqual(context.aws_request_id, "aws_request_id")
        self.assertIsInstance(context.log_group_name, str)
        self.assertEqual(context.log_stream_name, "log_stream_name")
        self.assertIsInstance(context.identity, context_module.MockCognitoIdentity)
        self.assertEqual(context.identity.cognito_identity_id, "identity_id")
        self.assertEqual(context.identity.cognito_identity_pool_id,
                         "identity_pool_id")
        self.assertIsInstance(context.client_context, context_module.MockClientContext)
        self.assertIsInstance(context.client_context.client,
                              context_module.MockClientContext.Client)
        self.assertEqual(context.client_context.client.installation_id,
                         "installation_id")
        self.assertEqual(context.client_context.client.app_title,
                         "app_title")
        self.assertEqual(context.client_context.client.app_version_name,
                         "app_version_name")
        self.assertEqual(context.client_context.client.app_version_code,
                         "app_version_code")
        self.assertEqual(context.client_context.client.app_package_name,
                         "app_package_name")
        self.assertEqual(context.client_context.custom,
                         {"custom_key": "custom_value"})
        self.assertEqual(context.client_context.env, {"env_key": "env_value"})

        context.activate(1)
        time.sleep(0.3)
        remaining = context.get_remaining_time_in_millis()
        self.assertLess(remaining, 750)
        self.assertGreater(remaining, 650)
        time.sleep(0.3)
        remaining = context.get_remaining_time_in_millis()
        self.assertLess(remaining, 450)
        self.assertGreater(remaining, 325)
        time.sleep(0.4)
        remaining = context.get_remaining_time_in_millis()
        self.assertLess(remaining, 50)
        self.assertGreaterEqual(remaining, 0)
        time.sleep(0.05)
        self.assertEqual(context.get_remaining_time_in_millis(), 0)

    def test_successful_call(self):
        def handle(event_arg, context_arg):
            return event["number"] + int(context.memory_limit_in_mb)
        event = {"number": 5, "other": "ignored"}
        context = context_module.MockLambdaContext.Builder()\
            .set_function_name("test_handle")\
            .set_memory_limit_in_mb("100")\
            .build()
        result = call_module.run_lambda(handle, event, context)
        self.assertIsInstance(result, call_module.LambdaResult)
        self.assertFalse(result.timed_out)
        self.assertIsNone(result.exception)
        self.assertEqual(result.value, 105)
        self.assertTrue(result.summary.duration_in_millis >= 0)
        self.assertIsInstance(result.summary.duration_in_millis, int)
        self.assertTrue(result.summary.max_memory_used_in_mb >= 0)
        self.assertIsInstance(result.summary.log, str)
        output = six.StringIO()
        result.display(output)

    def test_timeout_call(self):
        def handle(event_arg, context_arg):
            time.sleep(2)
        event = {}
        context = context_module.MockLambdaContext.Builder().build()
        result = call_module.run_lambda(handle, event, context,
                                        timeout_in_seconds=1)
        self.assertIsInstance(result, call_module.LambdaResult)
        self.assertTrue(result.timed_out)
        self.assertIsNone(result.exception)
        self.assertIsNone(result.value)

    def test_raising_call(self):
        def handle(event_arg, context_arg):
            raise ValueError(event)
        event = {"malformed": True}
        context = context_module.MockLambdaContext.Builder()\
            .set_identity(context_module.MockCognitoIdentity(
                identity_id="identity_id",
                identity_pool_id="identity_pool_id"
            ))\
            .build()
        result = call_module.run_lambda(handle, event, context, timeout_in_seconds=1)
        self.assertIsInstance(result, call_module.LambdaResult)
        self.assertFalse(result.timed_out)
        self.assertIsNone(result.value)
        self.assertIsInstance(result.exception, ValueError)

    def test_patches(self):
        event = {"number": 100}

        def mock_sqrt(n):
            return -1
        result = call_module.run_lambda(square_root.handle, event,
                                        patches={"math.sqrt": mock_sqrt},
                                        timeout_in_seconds=10)
        self.assertIsInstance(result, call_module.LambdaResult)
        self.assertFalse(result.timed_out)
        self.assertIsNone(result.exception)
        self.assertEqual(result.value, -1)
        self.assertGreater(math.sqrt(100), 9.9)  # check patch is gone


if __name__ == "__main__":
    unittest.main()
