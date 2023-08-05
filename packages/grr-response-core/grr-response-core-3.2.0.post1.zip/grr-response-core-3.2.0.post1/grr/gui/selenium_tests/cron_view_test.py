#!/usr/bin/env python
# -*- mode: python; encoding: utf-8 -*-
"""Test the cron_view interface."""



import unittest
from grr.gui import gui_test_lib
from grr.lib import flags
from grr.lib import rdfvalue
from grr.lib.rdfvalues import cronjobs as rdf_cronjobs
from grr.server import aff4
from grr.server.aff4_objects import cronjobs
from grr.server.flows.cron import system as cron_system
from grr.test_lib import test_lib


class TestCronView(gui_test_lib.GRRSeleniumTest):
  """Test the Cron view GUI."""

  def AddJobStatus(self, job_urn, status):
    with aff4.FACTORY.OpenWithLock(job_urn, token=self.token) as job:
      job.Set(job.Schema.LAST_RUN_TIME(rdfvalue.RDFDatetime.Now()))
      job.Set(job.Schema.LAST_RUN_STATUS(status=status))

  def setUp(self):
    super(TestCronView, self).setUp()

    for flow_name in [
        cron_system.GRRVersionBreakDown.__name__,
        cron_system.OSBreakDown.__name__, cron_system.LastAccessStats.__name__
    ]:
      cron_args = cronjobs.CreateCronJobFlowArgs(
          periodicity="7d", lifetime="1d")
      cron_args.flow_runner_args.flow_name = flow_name
      cronjobs.CRON_MANAGER.ScheduleFlow(
          cron_args, job_name=flow_name, token=self.token)

    cronjobs.CRON_MANAGER.RunOnce(token=self.token)

  def testCronView(self):
    self.Open("/")

    self.WaitUntil(self.IsElementPresent, "client_query")
    self.Click("css=a[grrtarget=crons]")

    # Table should contain Last Run
    self.WaitUntil(self.IsTextPresent, "Last Run")

    # Table should contain system cron jobs
    self.WaitUntil(self.IsTextPresent, cron_system.GRRVersionBreakDown.__name__)
    self.WaitUntil(self.IsTextPresent, cron_system.LastAccessStats.__name__)
    self.WaitUntil(self.IsTextPresent, cron_system.OSBreakDown.__name__)

    # Select a Cron.
    self.Click("css=td:contains('OSBreakDown')")

    # Check that there's one flow in the list.
    self.WaitUntil(self.IsElementPresent,
                   "css=#main_bottomPane td:contains('OSBreakDown')")

  def testMessageIsShownWhenNoCronJobSelected(self):
    self.Open("/")

    self.WaitUntil(self.IsElementPresent, "client_query")
    self.Click("css=a[grrtarget=crons]")

    self.WaitUntil(self.IsTextPresent,
                   "Please select a cron job to see the details.")

  def testShowsCronJobDetailsOnClick(self):
    self.Open("/")
    self.Click("css=a[grrtarget=crons]")
    self.Click("css=td:contains('OSBreakDown')")

    # Tabs should appear in the bottom pane
    self.WaitUntil(self.IsElementPresent, "css=#main_bottomPane #Details")
    self.WaitUntil(self.IsElementPresent, "css=#main_bottomPane #Flows")

    self.WaitUntil(self.IsTextPresent, "Allow Overruns")
    self.WaitUntil(self.IsTextPresent, "Flow Arguments")

    # Click on "Flows" tab
    self.Click("css=#main_bottomPane #Flows")

    # Click on the first flow and wait for flow details panel to appear.
    self.Click("css=#main_bottomPane td:contains('OSBreakDown')")
    self.WaitUntil(self.IsTextPresent, "Outstanding requests")

    # Close the panel.
    self.Click("css=#main_bottomPane .panel button.close")
    self.WaitUntilNot(self.IsTextPresent, "Outstanding requests")

  def testToolbarStateForDisabledCronJob(self):
    cronjobs.CRON_MANAGER.DisableJob(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    self.Open("/")
    self.Click("css=a[grrtarget=crons]")
    self.Click("css=td:contains('OSBreakDown')")

    self.assertTrue(
        self.IsElementPresent("css=button[name=EnableCronJob]:not([disabled])"))
    self.assertTrue(
        self.IsElementPresent("css=button[name=DisableCronJob][disabled]"))
    self.assertTrue(
        self.IsElementPresent("css=button[name=DeleteCronJob]:not([disabled])"))

  def testToolbarStateForEnabledCronJob(self):
    cronjobs.CRON_MANAGER.EnableJob(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    self.Open("/")
    self.Click("css=a[grrtarget=crons]")
    self.Click("css=td:contains('OSBreakDown')")

    self.assertTrue(
        self.IsElementPresent("css=button[name=EnableCronJob][disabled]"))
    self.assertTrue(
        self.IsElementPresent(
            "css=button[name=DisableCronJob]:not([disabled])"))
    self.assertTrue(
        self.IsElementPresent("css=button[name=DeleteCronJob]:not([disabled])"))

  def testEnableCronJob(self):
    cronjobs.CRON_MANAGER.DisableJob(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    self.Open("/")
    self.Click("css=a[grrtarget=crons]")
    self.Click("css=td:contains('OSBreakDown')")

    # Click on Enable button and check that dialog appears.
    self.Click("css=button[name=EnableCronJob]")
    self.WaitUntil(self.IsTextPresent,
                   "Are you sure you want to ENABLE this cron job?")

    # Click on "Proceed" and wait for authorization dialog to appear.
    self.Click("css=button[name=Proceed]")

    # This should be rejected now and a form request is made.
    self.WaitUntil(self.IsTextPresent, "Create a new approval")
    self.Click("css=grr-request-approval-dialog button[name=Cancel]")

    # Wait for dialog to disappear.
    self.WaitUntilNot(self.IsVisible, "css=.modal-open")

    self.GrantCronJobApproval(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    # Click on Enable button and check that dialog appears.
    self.Click("css=button[name=EnableCronJob]")
    self.WaitUntil(self.IsTextPresent,
                   "Are you sure you want to ENABLE this cron job?")

    # Click on "Proceed" and wait for success label to appear.
    # Also check that "Proceed" button gets disabled.
    self.Click("css=button[name=Proceed]")

    self.WaitUntil(self.IsTextPresent, "Cron job was ENABLED successfully!")
    self.assertFalse(self.IsElementPresent("css=button[name=Proceed]"))

    # Click on "Close" and check that dialog disappears.
    self.Click("css=button[name=Close]")
    self.WaitUntilNot(self.IsVisible, "css=.modal-open")

    # View should be refreshed automatically.
    self.WaitUntil(self.IsTextPresent, cron_system.OSBreakDown.__name__)
    self.WaitUntil(self.IsElementPresent,
                   "css=tr:contains('OSBreakDown') *[state=ENABLED]")

  def testDisableCronJob(self):
    cronjobs.CRON_MANAGER.EnableJob(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    self.Open("/")
    self.Click("css=a[grrtarget=crons]")
    self.Click("css=td:contains('OSBreakDown')")

    # Click on Enable button and check that dialog appears.
    self.Click("css=button[name=DisableCronJob]")
    self.WaitUntil(self.IsTextPresent,
                   "Are you sure you want to DISABLE this cron job?")

    # Click on "Proceed" and wait for authorization dialog to appear.
    self.Click("css=button[name=Proceed]")
    self.WaitUntil(self.IsTextPresent, "Create a new approval")

    self.Click("css=grr-request-approval-dialog button[name=Cancel]")
    # Wait for dialog to disappear.
    self.WaitUntilNot(self.IsVisible, "css=.modal-open")

    self.GrantCronJobApproval(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    # Click on Disable button and check that dialog appears.
    self.Click("css=button[name=DisableCronJob]")
    self.WaitUntil(self.IsTextPresent,
                   "Are you sure you want to DISABLE this cron job?")

    # Click on "Proceed" and wait for success label to appear.
    # Also check that "Proceed" button gets disabled.
    self.Click("css=button[name=Proceed]")

    self.WaitUntil(self.IsTextPresent, "Cron job was DISABLED successfully!")
    self.assertFalse(self.IsElementPresent("css=button[name=Proceed]"))

    # Click on "Close" and check that dialog disappears.
    self.Click("css=button[name=Close]")
    self.WaitUntilNot(self.IsVisible, "css=.modal-open")

    # View should be refreshed automatically.
    self.WaitUntil(self.IsTextPresent, cron_system.OSBreakDown.__name__)
    self.WaitUntil(self.IsElementPresent,
                   "css=tr:contains('OSBreakDown') *[state=DISABLED]")

  def testDeleteCronJob(self):
    cronjobs.CRON_MANAGER.EnableJob(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    self.Open("/")
    self.Click("css=a[grrtarget=crons]")
    self.Click("css=td:contains('OSBreakDown')")

    # Click on Delete button and check that dialog appears.
    self.Click("css=button[name=DeleteCronJob]:not([disabled])")
    self.WaitUntil(self.IsTextPresent,
                   "Are you sure you want to DELETE this cron job?")

    # Click on "Proceed" and wait for authorization dialog to appear.
    self.Click("css=button[name=Proceed]")
    self.WaitUntil(self.IsTextPresent, "Create a new approval")

    self.Click("css=grr-request-approval-dialog button[name=Cancel]")
    # Wait for dialog to disappear.
    self.WaitUntilNot(self.IsVisible, "css=.modal-open")

    self.GrantCronJobApproval(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    # Click on Delete button and check that dialog appears.
    self.Click("css=button[name=DeleteCronJob]:not([disabled])")
    self.WaitUntil(self.IsTextPresent,
                   "Are you sure you want to DELETE this cron job?")

    # Click on "Proceed" and wait for success label to appear.
    # Also check that "Proceed" button gets disabled.
    self.Click("css=button[name=Proceed]")

    self.WaitUntil(self.IsTextPresent, "Cron job was deleted successfully!")
    self.assertFalse(self.IsElementPresent("css=button[name=Proceed]"))

    # Click on "Close" and check that dialog disappears.
    self.Click("css=button[name=Close]")
    self.WaitUntilNot(self.IsVisible, "css=.modal-open")

    # View should be refreshed automatically.
    self.WaitUntil(self.IsElementPresent, "css=grr-cron-jobs-list "
                   "td:contains('GRRVersionBreakDown')")
    self.WaitUntilNot(self.IsElementPresent, "css=grr-cron-jobs-list "
                      "td:contains('OSBreakDown')")

  def testForceRunCronJob(self):
    cronjobs.CRON_MANAGER.EnableJob(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

    with test_lib.FakeTime(
        # 2274264646 corresponds to Sat, 25 Jan 2042 12:10:46 GMT.
        rdfvalue.RDFDatetime().FromSecondsFromEpoch(2274264646),
        increment=1e-6):
      self.Open("/")
      self.Click("css=a[grrtarget=crons]")
      self.Click("css=td:contains('OSBreakDown')")

      # Click on Force Run button and check that dialog appears.
      self.Click("css=button[name=ForceRunCronJob]:not([disabled])")
      self.WaitUntil(self.IsTextPresent,
                     "Are you sure you want to FORCE-RUN this cron job?")

      # Click on "Proceed" and wait for authorization dialog to appear.
      self.Click("css=button[name=Proceed]")
      self.WaitUntil(self.IsTextPresent, "Create a new approval")

      self.Click("css=grr-request-approval-dialog button[name=Cancel]")
      # Wait for dialog to disappear.
      self.WaitUntilNot(self.IsVisible, "css=.modal-open")

      self.GrantCronJobApproval(rdfvalue.RDFURN("aff4:/cron/OSBreakDown"))

      # Click on Force Run button and check that dialog appears.
      self.Click("css=button[name=ForceRunCronJob]:not([disabled])")
      self.WaitUntil(self.IsTextPresent,
                     "Are you sure you want to FORCE-RUN this cron job?")

      # Click on "Proceed" and wait for success label to appear.
      # Also check that "Proceed" button gets disabled.
      self.Click("css=button[name=Proceed]")

      self.WaitUntil(self.IsTextPresent,
                     "Cron job flow was FORCE-STARTED successfully!")
      self.assertFalse(self.IsElementPresent("css=button[name=Proceed]"))

      # Click on "Close" and check that dialog disappears.
      self.Click("css=button[name=Close]")
      self.WaitUntilNot(self.IsVisible, "css=.modal-open")

      # View should be refreshed automatically. The last run date should appear.
      self.WaitUntil(self.IsElementPresent, "css=grr-cron-jobs-list "
                     "tr:contains('OSBreakDown') td:contains('2042')")

  def testStuckCronJobIsHighlighted(self):
    # Make sure a lot of time has passed since the last
    # execution
    with test_lib.FakeTime(0):
      self.AddJobStatus("aff4:/cron/OSBreakDown",
                        rdf_cronjobs.CronJobRunStatus.Status.OK)

    self.Open("/")

    self.WaitUntil(self.IsElementPresent, "client_query")
    self.Click("css=a[grrtarget=crons]")

    # OSBreakDown's row should have a 'warn' class
    self.WaitUntil(self.IsElementPresent,
                   "css=tr.warning td:contains('OSBreakDown')")

    # Check that only OSBreakDown is highlighted
    self.WaitUntilNot(self.IsElementPresent,
                      "css=tr.warning td:contains('GRRVersionBreakDown')")

  def testFailingCronJobIsHighlighted(self):
    for _ in range(4):
      self.AddJobStatus("aff4:/cron/OSBreakDown",
                        rdf_cronjobs.CronJobRunStatus.Status.ERROR)

    self.Open("/")

    self.WaitUntil(self.IsElementPresent, "client_query")
    self.Click("css=a[grrtarget=crons]")

    # OSBreakDown's row should have an 'error' class
    self.WaitUntil(self.IsElementPresent,
                   "css=tr.danger td:contains('OSBreakDown')")
    # Check that only OSBreakDown is highlighted
    self.WaitUntilNot(self.IsElementPresent,
                      "css=tr.danger td:contains('GRRVersionBreakDown')")

  def testCronJobNotificationIsShownAndClickable(self):
    self._SendNotification("ViewObject", "aff4:/cron/OSBreakDown",
                           "Test CronJob notification")

    self.Open("/")

    self.Click("css=button[id=notification_button]")
    self.Click("css=a:contains('Test CronJob notification')")

    self.WaitUntil(self.IsElementPresent,
                   "css=tr.row-selected td:contains('OSBreakDown')")
    self.WaitUntil(self.IsElementPresent, "css=dd:contains('OSBreakDown')")


def main(argv):
  del argv  # Unused.
  # Run the full test suite
  unittest.main()


if __name__ == "__main__":
  flags.StartMain(main)
