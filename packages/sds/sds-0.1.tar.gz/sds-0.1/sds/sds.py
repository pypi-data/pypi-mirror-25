from collections import namedtuple
import itertools
import collections
import functools
import itertools
import random
class Agent:

	__slots__ = ('hypothesis','active')

	def __init__(self, hypothesis, active):

		self.hypothesis = hypothesis

		self.active = active

	@staticmethod
	def initialise(agent_count):

		return [
			Agent(hypothesis=None, active=False)
			for _
			in range(agent_count)
		]
ReadOnlyAgent = namedtuple("ReadOnlyAgent",("hypothesis","active"))
def generic_test_phase(
	swarm,
	microtests,
	random,
	multitesting,
	multitest_function,
	scalar
):

	def make_test(hyp): return multitest_function(
		random.choice(microtests)(hyp)
		for test_num
		in range(multitesting)
	)

	test_results = (
		make_test(agent.hypothesis)
		for agent
		in swarm
	)

	if scalar:

		test_results = list(test_results)

		test_results = [
			test_result > random.choice(test_results)
			for test_result
			in test_results
		]

	for agent, test_result in zip(swarm, test_results):

		agent.active = test_result
def test_phase(
	swarm,
	microtests,
	random,
	multitesting=1,
	multitest_function=lambda scores: next(x for x in scores),
):

	generic_test_phase(
		swarm=swarm,
		microtests=microtests,
		random=random,
		multitesting=multitesting,
		multitest_function=multitest_function,
		scalar=False,
	)
def scalar_test_phase(
	swarm,
	microtests,
	random,
	multitesting=1,
	multitest_function=lambda scores: next(x for x in scores),
):

	generic_test_phase(
		swarm=swarm,
		microtests=microtests,
		random=random,
		multitesting=multitesting,
		multitest_function=multitest_function,
		scalar=True,
	)
def generic_diffusion(
	swarm,
	random_hypothesis_function,
	random,
	context_free,
	context_sensitive,
	multidiffusion,
):

	if context_sensitive:
		context_free = True

	if context_free:
		old_swarm = [ReadOnlyAgent(a.hypothesis,a.active) for a in swarm]
	else:
		old_swarm = swarm

	for agent in swarm:

		polled_agents = (
			random.choice(old_swarm)
			for diffusion_num
			in range(int(multidiffusion))
		)

		for polled_agent in polled_agents:
			if polled_agent.active:
				break
		else:
			remainder = multidiffusion - int(multidiffusion)

			if remainder > 0:

				polled_agent = random.choice(old_swarm)

				if random.random() > remainder:

					polled_agent = ReadOnlyAgent(None,False)

		if (not agent.active and polled_agent.active):
			agent.hypothesis = polled_agent.hypothesis
		elif (
			not agent.active
			or polled_agent.active
			and context_free
			and (
				not context_sensitive
				or agent.hypothesis == polled_agent.hypothesis
			)
		):
			agent.active = False
			agent.hypothesis = random_hypothesis_function(random)
def passive_diffusion(
	swarm,
	random,
	random_hypothesis_function,
	multidiffusion=1,
):

	generic_diffusion(
		swarm,
		random_hypothesis_function,
		random,
		context_free=False,
		context_sensitive=False,
		multidiffusion=multidiffusion,
	)
def context_free_diffusion(
	swarm,
	random,
	random_hypothesis_function,
	multidiffusion=1,
):

	generic_diffusion(
		swarm,
		random_hypothesis_function,
		random,
		context_free=True,
		context_sensitive=False,
		multidiffusion=multidiffusion,
	)
def context_sensitive_diffusion(
	swarm,
	random,
	random_hypothesis_function,
	multidiffusion=1
):

	generic_diffusion(
		swarm,
		random_hypothesis_function,
		random,
		context_free=True,
		context_sensitive=True,
		multidiffusion=multidiffusion,
	)
def iterate(
	swarm,
	microtests,
	random_hypothesis_function,
	diffusion_function,
	random,
	test_phase_function=test_phase,
):
	diffusion_function(swarm, random, random_hypothesis_function)

	test_phase_function(swarm, microtests, random)
def never_halt(*args, **kwargs):
	return False
def make_stability_halting_function(lower, region, time):

	def generator_front_end(activity_count, halt_generator):
		next(halt_generator)
		halted = halt_generator.send(activity_count)
		return halted

	def is_stable_generator(lower, region, time):

		success_count = 0

		while True:

			swarm = yield

			active_count = sum(1 for agent in swarm if agent.active)/len(swarm)

			if active_count < lower or active_count > lower + region:
				success_count = 0
			else:
				success_count += 1
			
			yield success_count >= time

	halting_generator = is_stable_generator(lower, region, time)

	return functools.partial(
		generator_front_end,
		halt_generator=halting_generator,)
def make_instant_threshold_halt_function(threshold):
	def threshold_halt_function(swarm, threshold):

		activity = sum(1 for agent in swarm if agent.active)/len(swarm)

		return activity > threshold

	return functools.partial(threshold_halt_function,threshold=threshold)
def make_threshold_time_halting_function(lower, time):

	def generator_front_end(activity_count, halt_generator):
		next(halt_generator)
		halted = halt_generator.send(activity_count)
		return halted

	def is_stable_generator(lower, time):

		success_count = 0

		while True:

			swarm = yield

			active_count = sum(1 for agent in swarm if agent.active)/len(swarm)

			if active_count < lower:
				success_count = 0
			else:
				success_count += 1
			
			yield success_count >= time

	halting_generator = is_stable_generator(lower, time)

	return functools.partial(
		generator_front_end,
		halt_generator=halting_generator,)
def run(
	swarm,
	microtests,
	random_hypothesis_function,
	max_iterations,
	diffusion_function,
	random,
	halting_function=never_halt,
	halting_iterations=0,
	multitesting=1,
	multitest_function=all,
	report_iterations=None,
	test_phase_function=test_phase,
	hypothesis_string_function=str,
	max_cluster_report=None,
):

	if max_iterations is None:

		iterator = itertools.count()

	else:

		iterator = range(max_iterations)

	try:

		for iteration in iterator:

			diffusion_function(
				swarm=swarm,
				random=random,
				random_hypothesis_function=random_hypothesis_function,
			)

			test_phase_function(
				swarm=swarm,
				microtests=microtests,
				random=random,
				multitesting=multitesting,
				multitest_function=multitest_function,
			)

			if halting_iterations:

				if iteration % halting_iterations == 0:

					halts = halting_function(swarm)

					if halts:
						
						break

			if report_iterations:

				if iteration % report_iterations == 0:

					clusters = count_clusters(swarm)

					agent_count = len(swarm)

					print("{i:4} Activity: {a:0.3f}. {c}".format(
						i=iteration,
						a=sum(clusters.values())/float(agent_count),
						c=", ".join(
							"{hyp}:{count}".format(
								hyp=hypothesis_string_function(hyp),
								count=count
							)
							for hyp,count
							in clusters.most_common(max_cluster_report)
						),
					))

	except KeyboardInterrupt:

		pass

	return count_clusters(swarm)
def coupled_diffusion(
	swarms,
	random,
	random_hypothesis_functions,
	diffusion_functions,
):
	for swarm, diffusion_function, random_hypothesis_function in zip(
		swarms,
		diffusion_functions,
		random_hypothesis_functions
	):
		diffusion_function(swarm, random, random_hypothesis_function)
def generic_coupled_test_phase(
	master_swarm_num,
	swarms,
	random,
	multitesting,
	multitest_function,
	microtests,
	scalar,
):

	if not multitesting == 1:
		raise NotImplementedError(
			"Sorry, I've not got around to multitesting for coupled "
			"sds yet.")

	test_results = []

	tested_agents = []

	for master_agent in swarms[master_swarm_num]:

		agents = [random.choice(swarm) for swarm in swarms]

		agents[master_swarm_num] = master_agent

		hypotheses = tuple(agent.hypothesis for agent in agents)

		microtest = random.choice(microtests)

		test_results.append(microtest(*hypotheses))

		tested_agents.append(agents)

	if False and scalar:

		test_results = [
			test_result > random.choice(test_results)
			for test_result
			in test_results
		]

	for test_result, agents in zip(test_results, tested_agents):

		for agent in agents:

			agent.active = test_result
# master/slave synchronisation
def synchronous_coupled_test_phase(
	swarms,
	random,
	multitesting,
	multitest_function,
	microtests,
	scalar,
):
	master_swarm_num = 0

	generic_coupled_test_phase(
		master_swarm_num,
		swarms,
		random,
		multitesting,
		multitest_function,
		microtests,
		scalar,
	)
def sequential_coupled_test_phase(
	swarms,
	random,
	multitesting,
	multitest_function,
	microtests,
	scalar,
):
	for master_swarm_num in range(len(swarms)):

		generic_coupled_test_phase(
			master_swarm_num,
			swarms,
			random,
			multitesting,
			multitest_function,
			microtests,
			scalar,
		)
def iterate_coupled(
	swarms,
	random_hypothesis_functions,
	diffusion_functions,
	random,
	multitesting,
	multitest_function,
	report_iterations,
	test_phase_function,
	microtests,
	scalar,
):
	coupled_diffusion(
		swarms,
		random,
		random_hypothesis_functions,
		diffusion_functions)

	test_phase_function(
		swarms,
		random,
		multitesting,
		multitest_function,
		microtests,
		scalar,
	)
def run_coupled(
	swarms,
	random_hypothesis_functions,
	max_iterations,
	diffusion_functions,
	random,
	multitesting,
	multitest_function,
	report_iterations,
	test_phase_function,
	hypothesis_string_function,
	max_cluster_report,
	microtests,
	scalar,
):
	if max_iterations is None:

		iterator = itertools.count()

	else:

		iterator = range(max_iterations)

	try:

		for iteration in iterator:

			iterate_coupled(
				swarms,
				random_hypothesis_functions,
				diffusion_functions,
				random,
				multitesting,
				multitest_function,
				report_iterations,
				test_phase_function,
				microtests,
				scalar,
			)

			if report_iterations and iteration % report_iterations == 0:

				clusters_list = tuple(count_clusters(swarm) for swarm in swarms)

				agent_counts = tuple(len(swarm) for swarm in swarms)

				active_count = tuple(
					sum(clusters.values())
					for clusters
					in clusters_list)

				print(agent_counts,active_count,clusters_list)

	except KeyboardInterrupt:

		pass

	return tuple(count_clusters(swarm) for swarm in swarms)
def count_clusters(swarm):

	return collections.Counter(
		agent.hypothesis
		for agent
		in swarm
		if agent.active
	)
def activity(swarm):

	agent_count = len(swarm)

	active_count = sum(1 for agent in swarm if agent.active)

	return active_count/agent_count
def estimate_noise(
	microtests,
	random_hypothesis_function,
	noise_agent_count=100,
	iterations=100,
):

	def no_diffusion(swarm, random, random_hypothesis_function):
		for agent in swarm:
			agent.active = False
			agent.hypothesis = random_hypothesis_function(random)
	
	noise_swarm = Agent.initialise(100)

	activities = []

	for iteration in range(iterations):
		iterate(
			noise_swarm,
			microtests,
			random_hypothesis_function,
			no_diffusion,
			random,)

		activities.append(activity(noise_swarm))

	return sum(activities)/iterations
def swarm_from_clusters(agent_count, clusters):

	active_agents = (
		(
			Agent(hypothesis=hyp,active=True)
			for _ in
			range(count)
		)
		for hyp, count
		in clusters.items())

	inactive_count = agent_count - sum(clusters.values())

	return (
		Agent.initialise(inactive_count)
		+ list(itertools.chain.from_iterable(active_agents)))
def pretty_print_with_values(clusters, search_space, max_clusters=None):

	string_template = "{c:6d} at hyp {h:6d} (value: {e:0.6f})"

	cluster_strings = [
		string_template.format(
			c=count,
			h=hyp,
			e=search_space[hyp])
		for hyp, count
		in clusters.most_common(max_clusters)
	]

	return "\n".join(cluster_strings)
def simulate(
	scores,
	max_iterations=1000,
	report_iterations=500,
	diffusion_function=passive_diffusion,
	agent_count=1000,
	multitesting=1,
	multitest_function=all,
	random=random,
	random_hyp=None,
	halting_function=never_halt,
	halting_iterations=None,
):

	if random_hyp is None:

		def random_hyp(rnd): return rnd.randrange(1,len(scores))

	if halting_iterations is None:
		halting_iterations = report_iterations

	def make_microtest(test_num, rnd):
		return lambda hyp: rnd.random() < scores[test_num]

	microtests = [
		lambda hyp: random.random() < scores[hyp]
	]

	swarm=Agent.initialise(agent_count=agent_count)

	swarm[0].active = True
	swarm[0].hypothesis = 0

	clusters = run(
		swarm=swarm,
		microtests=microtests,
		random_hypothesis_function=random_hyp,
		max_iterations=max_iterations,
		diffusion_function=passive_diffusion,
		multitesting=multitesting,
		multitest_function=multitest_function,
		random=random,
		report_iterations=report_iterations,
		halting_function=halting_function,
		halting_iterations=halting_iterations,
	)

	return clusters
class Swarm:
	def __init__(self, size, random_hypothesis_function, lower_layer=None):

		self.agents = [
			Agent(active=False, hypothesis=None)
			for _
			in range(size)
		]

		if lower_layer is None:

			lower_layer = []

		self.lower_layer = lower_layer

		self.random_hypothesis = random_hypothesis_function

	@staticmethod
	def passive_diffusion(swarm, solitarity, random):

		for agent_num, agent in enumerate(swarm.agents):

			if not agent.active:

				polled_agent = random.choice(swarm.agents)

				if polled_agent.active and random.random() > solitarity:

					swarm.set_hypothesis(agent_num, polled_agent.hypothesis)

				else:

					agent.hypothesis = swarm.random_hypothesis(
						agent_num,
						random,
					)

	@staticmethod
	def context_free_diffusion(swarm, random):

		for agent_num, agent in enumerate(swarm.agents):

			polled_agent = random.choice(swarm.agents)

			if agent.active:

				if polled_agent.active:

					swarm.set_activity(agent_num, False)

					agent.hypothesis = swarm.random_hypothesis(
						agent_num,
						random,
					)

			else:

				if polled_agent.active:

					swarm.set_hypothesis(agent_num, polled_agent.hypothesis)

				else:

					agent.hypothesis = swarm.random_hypothesis(
						agent_num,
						random,
					)

	@staticmethod
	def context_sensitive_diffusion(swarm, random):

		for agent_num, agent in enumerate(swarm.agents):

			polled_agent = random.choice(swarm.agents)

			if agent.active:

				if (
					polled_agent.active
					and (agent.hypothesis == polled_agent.hypothesis)
				):


					swarm.set_activity(agent_num, False)

					agent.hypothesis = swarm.random_hypothesis(
						agent_num,
						random,
					)

			else:

				if polled_agent.active:

					swarm.set_hypothesis(agent_num, polled_agent.hypothesis)

				else:

					agent.hypothesis = swarm.random_hypothesis(
						agent_num,
						random,
					)

	def test(self, microtests, random, multitest=1, multitest_fun=None):

		for num, agent in enumerate(self.agents):

			microtest = random.choice(microtests)

			if multitest == 1:

				self.set_activity(num, microtest(agent.hypothesis))

			else:

				self.set_activity(
					num,
					multitest_fun(
						random.choice(microtests)(agent.hypothesis)
						for _
						in range(multitest)
					)
				)



	def iterate(
		self,
		microtests,
		random,
		diffusion_function=passive_diffusion.__func__,
		multitest=1,
		multitest_fun=None,
		solitarity=1,
	):
		diffusion_function(self, solitarity, random)
		self.test(microtests, random, multitest, multitest_fun)

	def set_activity(self, agent_num, new_activity):

		self.agents[agent_num].active = new_activity

		for swarm in self.lower_layer:

			swarm.set_activity(agent_num, new_activity)

	def set_hypothesis(self, agent_num, new_hypothesis):

		self.agents[agent_num].hypothesis = new_hypothesis

		if len(self.lower_layer) == 0:
			return

		for lower_swarm, hypothesis_component in (
			zip(self.lower_layer,new_hypothesis)):

			lower_swarm.set_hypothesis(agent_num, hypothesis_component)
def make_ml_sds(swarm_size, bottom_hyp_functions, topology):

	lower_layer = [
		Swarm(
			size=swarm_size,
			random_hypothesis_function=hyp_fun
		)
		for hyp_fun
		in bottom_hyp_functions
	]

	for layer_num, swarm_splits in enumerate(topology,start=1):

		layer = []

		swarm_offset = 0

		for split_num, swarm_split in enumerate(swarm_splits):

			lower_layer_start = swarm_offset

			lower_layer_end = swarm_offset+swarm_split

			random_hypothesis_function = functools.partial(
				random_compound_hyp,
				lower_layer[lower_layer_start:lower_layer_end],
			)

			new_swarm = Swarm(
				size=swarm_size,
				lower_layer=lower_layer[lower_layer_start:lower_layer_end],
				random_hypothesis_function=random_hypothesis_function)

			layer.append(new_swarm)

			swarm_offset += swarm_split

		lower_layer = layer

	top_swarm = lower_layer[0]

	return top_swarm
def single_diffusion(agent_num, swarm, random):

	# agent is guaranteed to be inactive
	agent = swarm.agents[agent_num]

	polled_agent = random.choice(swarm.agents)

	if polled_agent.active:

		swarm.set_hypothesis(agent_num,polled_agent.hypothesis)

		return polled_agent.hypothesis

	else:

		new_hyp = swarm.random_hypothesis(agent_num, random)

		agent.hypothesis = new_hyp

		return new_hyp
def random_compound_hyp(lower_swarms, num, random):

	return tuple(
		single_diffusion(num, lower_swarm, random)
		for lower_swarm
		in lower_swarms
	)
def flatten_hypothesis(hypothesis,times):
	new_hypothesis = itertools.chain.from_iterable(hypothesis)
	if times == 1:
		return list(new_hypothesis)
	else:
		return flatten_hypothesis(new_hypothesis,times-1)
