#!/usr/bin/env python
"""Test of "Copy Hunt" wizard."""


import unittest
from grr.gui import gui_test_lib

from grr.lib import flags
from grr.lib.rdfvalues import file_finder as rdf_file_finder
from grr.lib.rdfvalues import flows as rdf_flows
from grr.lib.rdfvalues import paths as rdf_paths
from grr.server import aff4
from grr.server import foreman as rdf_foreman
from grr.server import output_plugin
from grr.server.flows.general import file_finder
from grr.server.flows.general import transfer
from grr.server.hunts import implementation
from grr.server.hunts import standard


class HuntCopyTest(gui_test_lib.GRRSeleniumTest):
  """Test the hunt copying GUI."""

  @staticmethod
  def CreateSampleHunt(description, token=None):
    implementation.GRRHunt.StartHunt(
        hunt_name=standard.GenericHunt.__name__,
        description=description,
        flow_runner_args=rdf_flows.FlowRunnerArgs(
            flow_name=transfer.GetFile.__name__),
        flow_args=transfer.GetFileArgs(pathspec=rdf_paths.PathSpec(
            path="/tmp/evil.txt",
            pathtype=rdf_paths.PathSpec.PathType.TSK,)),
        client_rule_set=rdf_foreman.ForemanClientRuleSet(
            rules=[
                rdf_foreman.ForemanClientRule(
                    rule_type=rdf_foreman.ForemanClientRule.Type.REGEX,
                    regex=rdf_foreman.ForemanRegexClientRule(
                        attribute_name="GRR client", attribute_regex="GRR"))
            ]),
        output_plugins=[
            output_plugin.OutputPluginDescriptor(
                plugin_name="DummyOutputPlugin",
                plugin_args=gui_test_lib.DummyOutputPlugin.args_type(
                    filename_regex="blah!", fetch_binaries=True))
        ],
        client_rate=60,
        token=token)

  def testCopyHuntPrefillsNewHuntWizard(self):
    self.CreateSampleHunt("model hunt", token=self.token)

    self.Open("/#main=ManageHunts")
    self.Click("css=tr:contains('model hunt')")
    self.Click("css=button[name=CopyHunt]:not([disabled])")

    # Wait until dialog appears.
    self.WaitUntil(self.IsTextPresent, "What to run?")

    # Check that non-default values of sample hunt are prefilled.
    self.WaitUntilEqual("/tmp/evil.txt", self.GetValue,
                        "css=grr-new-hunt-wizard-form "
                        "label:contains('Path') ~ * input:text")

    self.WaitUntilEqual("TSK", self.GetText, "css=grr-new-hunt-wizard-form "
                        "label:contains('Pathtype') ~ * select option:selected")

    self.WaitUntilEqual("model hunt (copy)", self.GetValue,
                        "css=grr-new-hunt-wizard-form "
                        "label:contains('Description') ~ * input:text")

    self.WaitUntilEqual("60", self.GetValue, "css=grr-new-hunt-wizard-form "
                        "label:contains('Client rate') ~ * input")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Output Processing")

    # Check that output plugins list is prefilled.
    self.WaitUntilEqual("DummyOutputPlugin", self.GetText,
                        "css=grr-new-hunt-wizard-form "
                        "label:contains('Plugin') ~ * select option:selected")

    self.WaitUntilEqual("blah!", self.GetValue, "css=grr-new-hunt-wizard-form "
                        "label:contains('Filename Regex') ~ * input:text")

    self.WaitUntil(self.IsElementPresent, "css=grr-new-hunt-wizard-form "
                   "label:contains('Fetch Binaries') ~ * input:checked")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Where to run?")

    # Check that rules list is prefilled.
    self.WaitUntilEqual("Regex", self.GetText, "css=grr-new-hunt-wizard-form "
                        "label:contains('Rule type') "
                        "~ * select option:selected")

    self.WaitUntilEqual("GRR client", self.GetText,
                        "css=grr-new-hunt-wizard-form "
                        "label:contains('Attribute name') "
                        "~ * select option:selected")

    self.WaitUntilEqual("GRR", self.GetValue, "css=grr-new-hunt-wizard-form "
                        "label:contains('Attribute regex') ~ * input:text")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Review")

    # Check that review page contains expected values.
    self.WaitUntil(self.IsTextPresent, "TSK")
    self.WaitUntil(self.IsTextPresent, "/tmp/evil.txt")
    self.WaitUntil(self.IsTextPresent, transfer.GetFile.__name__)
    self.WaitUntil(self.IsTextPresent, "DummyOutputPlugin")
    self.WaitUntil(self.IsTextPresent, "blah!")
    self.WaitUntil(self.IsTextPresent, "model hunt (copy)")
    self.WaitUntil(self.IsTextPresent, "GRR client")
    self.WaitUntil(self.IsTextPresent, "60")

  def testCopyHuntCreatesExactCopyWithChangedDescription(self):
    self.CreateSampleHunt("model hunt", token=self.token)

    self.Open("/#main=ManageHunts")
    self.Click("css=tr:contains('model hunt')")
    self.Click("css=button[name=CopyHunt]:not([disabled])")

    # Wait until dialog appears and then click through.
    self.WaitUntil(self.IsTextPresent, "What to run?")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Output Processing")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Where to run?")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Review")

    # Click on "Run" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Created Hunt")

    hunts_root = aff4.FACTORY.Open("aff4:/hunts", token=self.token)
    hunts_list = sorted(list(hunts_root.ListChildren()), key=lambda x: x.age)

    self.assertEqual(len(hunts_list), 2)

    first_hunt = aff4.FACTORY.Open(hunts_list[0], token=self.token)
    last_hunt = aff4.FACTORY.Open(hunts_list[1], token=self.token)

    # Check that generic hunt arguments are equal.
    self.assertEqual(first_hunt.args, last_hunt.args)

    # Check that hunts runner arguments are equal except for the description.
    # Hunt copy has ' (copy)' added to the description.
    first_runner_args = first_hunt.runner_args
    last_runner_args = last_hunt.runner_args

    self.assertEqual(first_runner_args.description + " (copy)",
                     last_runner_args.description)
    self.assertEqual(first_runner_args.client_rate,
                     last_runner_args.client_rate)
    self.assertEqual(first_runner_args.hunt_name, last_runner_args.hunt_name)
    self.assertEqual(first_runner_args.client_rule_set,
                     last_runner_args.client_rule_set)

  def testCopyHuntRespectsUserChanges(self):
    self.CreateSampleHunt("model hunt", token=self.token)

    self.Open("/#main=ManageHunts")
    self.Click("css=tr:contains('model hunt')")
    self.Click("css=button[name=CopyHunt]:not([disabled])")

    # Wait until dialog appears and then click through.
    self.WaitUntil(self.IsTextPresent, "What to run?")

    # Change values in the flow configuration.
    self.Type("css=grr-new-hunt-wizard-form label:contains('Path') "
              "~ * input:text", "/tmp/very-evil.txt")

    self.Select("css=grr-new-hunt-wizard-form label:contains('Pathtype') "
                "~ * select", "OS")

    self.Type("css=grr-new-hunt-wizard-form label:contains('Description') "
              "~ * input:text", "my personal copy")

    self.Type("css=grr-new-hunt-wizard-form label:contains('Client rate') "
              "~ * input", "42")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Output Processing")

    # Change output plugin and add another one.
    self.Click("css=grr-new-hunt-wizard-form button[name=Add]")
    self.Select("css=grr-configure-output-plugins-page select:eq(0)",
                "DummyOutputPlugin")
    self.Type("css=grr-configure-output-plugins-page "
              "label:contains('Filename Regex'):eq(0) ~ * input:text",
              "foobar!")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Where to run?")

    # Replace a rule with another one.
    self.Click("css=grr-configure-rules-page button[name=Remove]")
    self.Click("css=grr-configure-rules-page button[name=Add]")
    self.Click("css=grr-configure-rules-page label:contains('Os darwin') ~ * "
               "input[type=checkbox]")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Review")

    # Check that expected values are shown in the review.
    self.WaitUntil(self.IsTextPresent, "OS")
    self.WaitUntil(self.IsTextPresent, "/tmp/very-evil.txt")
    self.WaitUntil(self.IsTextPresent, transfer.GetFile.__name__)
    self.WaitUntil(self.IsTextPresent, "DummyOutputPlugin")
    self.WaitUntil(self.IsTextPresent, "foobar!")
    self.WaitUntil(self.IsTextPresent, "blah!")
    self.WaitUntil(self.IsTextPresent, "my personal copy")
    self.WaitUntil(self.IsTextPresent, "Os darwin")
    self.WaitUntil(self.IsTextPresent, "42")

    # Click on "Run" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Created Hunt")

    hunts_root = aff4.FACTORY.Open("aff4:/hunts", token=self.token)
    hunts_list = sorted(list(hunts_root.ListChildren()), key=lambda x: x.age)

    self.assertEqual(len(hunts_list), 2)
    last_hunt = aff4.FACTORY.Open(hunts_list[-1], token=self.token)

    self.assertEqual(last_hunt.args.flow_args.pathspec.path,
                     "/tmp/very-evil.txt")
    self.assertEqual(last_hunt.args.flow_args.pathspec.pathtype, "OS")
    self.assertEqual(last_hunt.args.flow_runner_args.flow_name,
                     transfer.GetFile.__name__)

    self.assertEqual(len(last_hunt.runner_args.output_plugins), 2)
    self.assertEqual(last_hunt.runner_args.output_plugins[0].plugin_name,
                     "DummyOutputPlugin")
    self.assertEqual(
        last_hunt.runner_args.output_plugins[0].plugin_args.filename_regex,
        "foobar!")
    self.assertEqual(
        last_hunt.runner_args.output_plugins[0].plugin_args.fetch_binaries,
        False)
    self.assertEqual(last_hunt.runner_args.output_plugins[1].plugin_name,
                     "DummyOutputPlugin")
    self.assertEqual(
        last_hunt.runner_args.output_plugins[1].plugin_args.filename_regex,
        "blah!")
    self.assertEqual(
        last_hunt.runner_args.output_plugins[1].plugin_args.fetch_binaries,
        True)

    runner_args = last_hunt.runner_args
    self.assertAlmostEqual(runner_args.client_rate, 42)
    self.assertEqual(runner_args.description, "my personal copy")
    self.assertEqual(
        runner_args.client_rule_set,
        rdf_foreman.ForemanClientRuleSet(rules=[
            rdf_foreman.ForemanClientRule(os=rdf_foreman.ForemanOsClientRule(
                os_darwin=True))
        ]))

  def testCopyHuntHandlesLiteralExpressionCorrectly(self):
    """Literals are raw bytes. Testing that raw bytes are processed right."""
    literal_match = rdf_file_finder.FileFinderContentsLiteralMatchCondition(
        literal="foo\x0d\xc8bar")

    implementation.GRRHunt.StartHunt(
        hunt_name=standard.GenericHunt.__name__,
        description="model hunt",
        flow_runner_args=rdf_flows.FlowRunnerArgs(
            flow_name=file_finder.FileFinder.__name__),
        flow_args=rdf_file_finder.FileFinderArgs(
            conditions=[
                rdf_file_finder.FileFinderCondition(
                    condition_type="CONTENTS_LITERAL_MATCH",
                    contents_literal_match=literal_match)
            ],
            paths=["/tmp/evil.txt"]),
        token=self.token)

    self.Open("/#main=ManageHunts")
    self.Click("css=tr:contains('model hunt')")
    self.Click("css=button[name=CopyHunt]:not([disabled])")

    # Wait until dialog appears.
    self.WaitUntil(self.IsTextPresent, "What to run?")

    # Check that non-default values of sample hunt are prefilled.
    self.WaitUntilEqual("foo\\x0d\\xc8bar", self.GetValue,
                        "css=grr-new-hunt-wizard-form "
                        "label:contains('Literal') ~ * input:text")

    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Output Processing")
    # Click on "Next" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Where to run?")
    # Click on "Next" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Review")

    # Check that the arguments summary is present.
    self.WaitUntil(self.IsTextPresent, file_finder.FileFinder.__name__)
    self.WaitUntil(self.IsTextPresent, "foo\\x0d\\xc8bar")

    # Click on "Run" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Created Hunt")
    # Close the window and check that the hunt was created.
    self.Click("css=button.Next")

    hunts_root = aff4.FACTORY.Open("aff4:/hunts", token=self.token)
    hunts_list = sorted(list(hunts_root.ListChildren()), key=lambda x: x.age)

    self.assertEqual(len(hunts_list), 2)
    last_hunt = aff4.FACTORY.Open(hunts_list[-1], token=self.token)

    # Check that the hunt was created with a correct literal value.
    self.assertEqual(last_hunt.args.flow_runner_args.flow_name,
                     file_finder.FileFinder.__name__)
    self.assertEqual(last_hunt.args.flow_args.conditions[0]
                     .contents_literal_match.literal, "foo\x0d\xc8bar")

  def testCopyHuntPreservesRuleType(self):
    implementation.GRRHunt.StartHunt(
        hunt_name=standard.GenericHunt.__name__,
        description="model hunt",
        flow_runner_args=rdf_flows.FlowRunnerArgs(
            flow_name=transfer.GetFile.__name__),
        flow_args=transfer.GetFileArgs(pathspec=rdf_paths.PathSpec(
            path="/tmp/evil.txt",
            pathtype=rdf_paths.PathSpec.PathType.TSK,)),
        client_rule_set=rdf_foreman.ForemanClientRuleSet(
            rules=[
                rdf_foreman.ForemanClientRule(
                    rule_type=rdf_foreman.ForemanClientRule.Type.OS,
                    os=rdf_foreman.ForemanOsClientRule(os_darwin=True))
            ]),
        token=self.token)

    self.Open("/#main=ManageHunts")
    self.Click("css=tr:contains('model hunt')")
    self.Click("css=button[name=CopyHunt]:not([disabled])")

    # Wait until dialog appears.
    self.WaitUntil(self.IsTextPresent, "What to run?")
    # Click on "Next" button.
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Output Processing")
    # Click on "Next" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Where to run?")
    self.WaitUntil(self.IsElementPresent, "css=grr-new-hunt-wizard-form "
                   "label:contains('Os darwin') ~ * input:checked")

  def testRuleTypeChangeClearsItsProto(self):
    # Open up and click on View Hunts.
    self.Open("/")
    self.Click("css=a[grrtarget=hunts]")

    # Open up "New Hunt" wizard
    self.Click("css=button[name=NewHunt]")

    # Click on Filesystem item in flows list
    self.Click("css=#_Filesystem > i.jstree-icon")

    # Click on the FileFinder item in Filesystem flows list
    self.Click("link=File Finder")

    # Click on "Next" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Output Processing")

    # Click on "Next" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Where to run?")

    # Changing the rule type clears the entered data under the hood.
    self.Click("css=grr-configure-rules-page button[name=Add]")
    self.Click("css=grr-configure-rules-page div.well:nth(0) "
               "label:contains('Os windows') ~ * input[type=checkbox]")
    self.Select("css=grr-configure-rules-page div.well:nth(0) select",
                "Integer")
    self.Type("css=grr-new-hunt-wizard-form "
              "grr-form-proto-repeated-field:has(label:contains('Path')) "
              "input", "/tmp")

    # Click on "Next" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")
    self.WaitUntil(self.IsTextPresent, "Review")

    # Click on "Run" button
    self.Click("css=grr-new-hunt-wizard-form button.Next")

    self.WaitUntil(self.IsTextPresent, "Created Hunt")
    # Close the window
    self.Click("css=button.Next")

    # Check that the hunt object was actually created
    hunts_root = aff4.FACTORY.Open("aff4:/hunts", token=self.token)
    hunts_list = list(hunts_root.OpenChildren())
    self.assertEqual(len(hunts_list), 1)

    hunt = hunts_list[0]

    # Check that the hunt was created with correct rules
    rules = hunt.runner_args.client_rule_set.rules
    self.assertEqual(len(rules), 1)
    rule = rules[0]

    self.assertEqual(rule.rule_type, rdf_foreman.ForemanClientRule.Type.INTEGER)
    self.assertEqual(rule.integer.path, "/tmp")

    # Assert that the deselected union field is cleared
    self.assertFalse(rule.os.os_windows)


def main(argv):
  del argv  # Unused.
  # Run the full test suite
  unittest.main()


if __name__ == "__main__":
  flags.StartMain(main)
