from batsim.batsim import BatsimScheduler
from sortedcontainers import SortedSet


class ValidatingMachine(BatsimScheduler):
    """
    This class tries to do a lot of checks to prevent from stupid and invisible errors.

    You should use this when you are developping and testing a scheduler.

    It checks that:
    - not 2 jobs use the same resource as the same time
    - a job is only started once
    - a job is launched after his submit time
    """

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def onAfterBatsimInit(self):
        self.scheduler.onAfterBatsimInit()

    def onSimulationBegins(self):
        self.nb_res = self.bs.nb_res
        self.availableResources = SortedSet(range(self.nb_res))
        self.jobs_waiting = []
        self.previousAllocations = dict()

        # intercept job start
        self.bs_start_jobs_continuous = self.bs.start_jobs_continuous
        self.bs.start_jobs_continuous = self.start_jobs_continuous
        self.bs_start_jobs = self.bs.start_jobs
        self.bs.start_jobs = self.start_jobs

        self.scheduler.bs = self.bs
        self.scheduler.onSimulationBegins()

    def onSimulationEnds(self):
        self.scheduler.onSimulationEnds()

    def onNOP(self):
        self.scheduler.onNOP()

    def onDeadlock(self):
        self.scheduler.onDeadlock()

    def onJobSubmission(self, job):
        self.jobs_waiting.append(job)
        self.scheduler.onJobSubmission(job)

    def onJobCompletion(self, job):
        for res in self.previousAllocations[job.id]:
            self.availableResources.add(res)
        self.previousAllocations.pop(job.id)
        self.scheduler.onJobCompletion(job)

    def onJobMessage(self, timestamp, job, message):
        self.scheduler.onJobMessage(timestamp, job, message)

    def onJobsKilled(self, jobs):
        self.scheduler.onJobsKilled(jobs)

    def onMachinePStateChanged(self, nodeid, pstate):
        self.scheduler.onMachinePStateChanged(nodeid, pstate)

    def onReportEnergyConsumed(self, consumed_energy):
        self.scheduler.onReportEnergyConsumed(consumed_energy)

    def start_jobs_continuous(self, allocs):
        for (job, (first_res, last_res)) in allocs:
            self.previousAllocations[job.id] = range(first_res, last_res + 1)
            self.jobs_waiting.remove(job)
            for r in range(first_res, last_res + 1):
                self.availableResources.remove(r)
        self.bs_start_jobs_continuous(allocs)

    def start_jobs(self, jobs, res):
        for j in jobs:
            self.jobs_waiting.remove(j)
            self.previousAllocations[j.id] = res[j.id]
            for r in res[j.id]:
                self.availableResources.remove(r)
        self.bs_start_jobs(jobs, res)
