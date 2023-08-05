#!/usr/bin/env python
"""Tests for the RegistryFinder flow."""


from grr.lib import flags
from grr.lib import utils
from grr.server import flow
from grr.server.flows.general import registry as flow_registry
from grr.test_lib import action_mocks
from grr.test_lib import flow_test_lib
from grr.test_lib import test_lib
from grr.test_lib import vfs_test_lib


class TestRegistryFinderFlow(flow_test_lib.FlowTestsBaseclass):
  """Test the RegistryFinder flow."""

  def setUp(self):
    super(TestRegistryFinderFlow, self).setUp()
    self.registry_stubber = vfs_test_lib.RegistryVFSStubber()
    self.registry_stubber.Start()

  def tearDown(self):
    super(TestRegistryFinderFlow, self).tearDown()
    self.registry_stubber.Stop()

  def _RunRegistryFinder(self, paths=None):
    client_mock = action_mocks.GlobClientMock()

    client_id = self.SetupClients(1)[0]

    for s in flow_test_lib.TestFlowHelper(
        flow_registry.RegistryFinder.__name__,
        client_mock,
        client_id=client_id,
        keys_paths=paths,
        conditions=[],
        token=self.token):
      session_id = s

    return list(
        flow.GRRFlow.ResultCollectionForFID(session_id, token=self.token))

  def testRegistryFinder(self):
    # Listing inside a key gives the values.
    results = self._RunRegistryFinder(
        ["HKEY_LOCAL_MACHINE/SOFTWARE/ListingTest/*"])
    self.assertEqual(len(results), 2)
    self.assertEqual(
        sorted([x.stat_entry.registry_data.GetValue()
                for x in results]), ["Value1", "Value2"])

    # This is a key so we should get back the default value.
    results = self._RunRegistryFinder(
        ["HKEY_LOCAL_MACHINE/SOFTWARE/ListingTest"])

    self.assertEqual(len(results), 1)
    self.assertEqual(results[0].stat_entry.registry_data.GetValue(),
                     "DefaultValue")

    # The same should work using a wildcard.
    results = self._RunRegistryFinder(["HKEY_LOCAL_MACHINE/SOFTWARE/*"])

    self.assertTrue(results)
    paths = [x.stat_entry.pathspec.path for x in results]
    expected_path = u"/HKEY_LOCAL_MACHINE/SOFTWARE/ListingTest"
    self.assertIn(expected_path, paths)
    idx = paths.index(expected_path)
    self.assertEqual(results[idx].stat_entry.registry_data.GetValue(),
                     "DefaultValue")

  def testListingRegistryKeysDoesNotYieldMTimes(self):
    # Just listing all keys does not generate a full stat entry for each of
    # the results.
    results = self._RunRegistryFinder(
        ["HKEY_LOCAL_MACHINE/SOFTWARE/ListingTest/*"])
    self.assertEqual(len(results), 2)
    for result in results:
      st = result.stat_entry
      self.assertIsNone(st.st_mtime)

    # Explicitly calling RegistryFinder on a value does though.
    results = self._RunRegistryFinder([
        "HKEY_LOCAL_MACHINE/SOFTWARE/ListingTest/Value1",
        "HKEY_LOCAL_MACHINE/SOFTWARE/ListingTest/Value2",
    ])

    self.assertEqual(len(results), 2)
    for result in results:
      st = result.stat_entry
      path = utils.SmartStr(st.pathspec.path)
      if "Value1" in path:
        self.assertEqual(st.st_mtime, 110)
      elif "Value2" in path:
        self.assertEqual(st.st_mtime, 120)
      else:
        self.fail("Unexpected value: %s" % path)


def main(argv):
  # Run the full test suite
  test_lib.main(argv)


if __name__ == "__main__":
  flags.StartMain(main)
