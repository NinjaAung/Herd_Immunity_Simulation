from person import Person
from logger import Logger
from virus import Virus
from uuid import uuid4
import random
import sys
random.seed(42)

class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.
    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.
        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.infected_pop = []
        self.dead = []
        self.vacc_pop = []
        self.norm_pop = []
        self.pop_size = pop_size
        self.pop_size_init = pop_size
        self.next_person_id = 0
        self.virus = virus
        self.initial_infected = initial_infected
        self.total_infected = initial_infected
        self.current_infected = self.initial_infected
        self.vacc_percentage = vacc_percentage
        self.total_vacc = int(vacc_percentage*self.pop_size)
        self.total_dead = 0
        self.population = self._create_population(initial_infected)
        self.file_name = f"{self.virus.name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt"
        self.newly_infected = []
        self._infect_newly_infected()
        self.logger = Logger(self.file_name)
        self.time_step_counter = 0
        self.total_inf = []

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.
            Returns:
                list: A list of Person objects.
        '''

        population = []
        for _ in range(initial_infected):
            infected_person = Person(uuid4(), False, self.virus)
            population.append(infected_person)
            self.infected_pop.append(infected_person)

        for _ in range(self.total_vacc):
            vacc_person = Person(uuid4(), True)
            population.append(vacc_person)
            self.vacc_pop.append(vacc_person)

        for _ in range(self.pop_size - self.total_vacc - initial_infected):
            norm_person = Person(uuid4(), False)
            self.norm_pop.append(norm_person)
            population.append(norm_person)

        return population


    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.

        if self.total_vacc + self.total_dead >= self.pop_size_init:
            should_continue = False
        else:
            should_continue = True
        return should_continue


    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
         # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
        self.logger.write_metadata(self.pop_size, self.vacc_percentage,
                                        self.virus.name, self.virus.mortality_rate,
                                        self.virus.repro_rate)

        should_continue = self._simulation_should_continue()
        while should_continue:
            self.time_step_counter += 1
            self.time_step()
            should_continue = self._simulation_should_continue()

        return print(f'The simulation has ended after {self.time_step_counter} turns.')

     def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.
        At the end of a time step, an infected person will either die of the infection or get better.
        The chance they will die is the percentage chance stored in mortality_rate.
        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        total_inf = self.total_infected_list()
        print(len(total_inf))
        for person in total_inf:
            # print(len(total_inf))
            if person.is_alive == True and person.infection:
                interactions = 0
                while interactions < 100:
                    random_person = random.choice(self.population)

                    if random_person._id != person._id and random_person.is_alive == True:
                        self.interaction(person, random_person)
                        interactions += 1
            self.did_survive(person)


        self._infect_newly_infected()

        self.logger.log_time_step(self.time_step_counter, self)

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.
        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''

        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated == False and random_person.infection == None and random_person._id not in self.newly_infected:
            random_person.infection = self.virus
            inf_chance = random.random()
            if inf_chance <= self.virus.repro_rate:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, True, False, True)
                self.current_infected += 1
                self.total_infected += 1
        elif random_person.is_vaccinated == True:
            self.logger.log_interaction(person, random_person, False , True, False)
        elif random_person.infection != None:
            self.logger.log_interaction(person, random_person, True, False, False)


    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

        for person in self.population:
            if person._id in self.newly_infected:
                person.infection = self.virus

        #reset newly_infected to an empty array
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_rate = float(params[4])


    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()
