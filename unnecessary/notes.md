## What is reinforcement learning

Reinforcement learning is learning what to do--how to map situations to actions--so as to maximize a reward signal. The learner is not told which actions to take, but instead must discover which actions yield the most reward by trying them. 

Beyond the agent and the environment, one can identify four main subelements of a reinforcement learning system: a policy, a reward signal, a value function, and, optionally, a model of the environment.
+ _policy_: defines the learning agent’s way of behaving at a given time
+ _reward signal_: defines the goal of a reinforcement learning problem
    + on each time step, the environment sends to the reinforcement learning agent a single number called the _reward_.
+ _value function_: whereas the reward signal indicates what is good in an immediate sense, a value function specifies what is good in the long run
    + the _value_ of a state is the total amount of reward an agent can expect to accumulate over the future, starting from that state
+ _model_: something that mimics the behavior of the environment, or more generally, that allows inferences to be made about how the environment will behave


