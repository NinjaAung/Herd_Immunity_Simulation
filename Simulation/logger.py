import os
from person import Person
from virus import Virus


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        # The file_name passed should be the full file name of the file that the logs will be written to
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''

        with open(self.file_name, 'w') as f:
                log_file_msg = f"""___MetaData___\nPopulation Size: {pop_size}\nVaccination Percentage: {vacc_percentage*100}%\nVirus: {virus_name}\nMortality Rate: {mortality_rate*100}%\nBasic Reproduction Number: {basic_repro_num*100}%\n\n____Simulation____\n\n"""
                f.write(log_file_msg)

        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.
        The format of the log should be: "{person.ID} infects {random_person.ID} \n"
        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        with open(self.file_name, 'a') as f:
            
            if did_infect and not random_person_vacc and not random_person_sick:
                log_file_msg = f"[Success]: {person._id} infected {random_person._id}.\n"
                f.write(log_file_msg)
            elif not did_infect:
                if random_person_vacc:
                    log_file_msg = f"[Fail]: {person._id} : {random_person._id} is [VACCINATED]\n"
                    f.write(log_file_msg)
                elif random_person_sick:
                    log_file_msg = f"[Fail]: {person._id} : {random_person._id} is already [SICK]\n"
                    f.write(log_file_msg)
                else:
                    log_file_msg = f"[FAIL]: {person._id} : {random_person._id} [RESISTED]\n"
                    f.write(log_file_msg)
        f.close()

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.
        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        with open(self.file_name, 'a') as f:
            if did_die_from_infection:
                log_file_msg = f"[Survived]: {person._id}\n"
                f.write(log_file_msg)
            elif not did_die_from_infection:
                log_file_msg = f"[Dead]: {person._id}\n"
                f.write(log_file_msg)

    def log_time_step(self, time_step_number, sim_data):
        ''' STRETCH CHALLENGE DETAILS:
        If you choose to extend this method, the format of the summary statistics logged
        are up to you.
        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.
        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        init_dead = sim_data.total_dead 
        newly_dead = sim_data.total_dead - init_dead
        init_infected = sim_data.total_infected
        newly_infected = sim_data.total_infected - init_infected

        with open(self.file_name, 'a') as f:
            time_step_msg = f"\n\nTime step {time_step_number} ended, beginning {time_step_number + 1}\nNumber of people Infected: {newly_infected}\nNewly Dead: {newly_dead}\nTotal Dead: {sim_data.total_dead}\nTotal Infected: {sim_data.total_infected}\ntotal Vaccinated: {sim_data.total_vacc}\ntotal pop alive: {sim_data.pop_size - sim_data.total_dead}\n"
            f.write(time_step_msg)