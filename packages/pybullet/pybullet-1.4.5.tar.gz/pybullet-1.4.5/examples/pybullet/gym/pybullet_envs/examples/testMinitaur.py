import pybullet_envs.bullet.minitaur_gym_env as minitaur_gym_env
import time

env = functools.partial(minitaur_gym_env.MinitaurBulletEnv, render=True)
env.init()
env.reset()
env.step()

while (1):
	p.stepSimulation()
	env.step()
