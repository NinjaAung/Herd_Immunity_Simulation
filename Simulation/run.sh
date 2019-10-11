
python3 simulation.py {population size} {vacc_percentage} {virus_name} {mortality_rate} {repro_rate} {number of people initially infected}

popsize=
vaccper=
name=
mortal=
repro=
intial=


usage()
{
    echo "usage: run [-h help] [-p population size ] [-v vacc_percentage] [-n name] [-m mortality_rate] [-r repro_rate] [-i intially_infected] "
    exit 1
}

function cleanUp()
{
    echo "\n${red}Error: Script Canceled"
    exit 2
}
read -p "[Population Size]: " popsize
read -p "[Vaccinated Percentage]: " vaccper
read -p "[Virus Name]: " name
read -p "[Mortality Rate]: " mortal
read -p "[Reproduction Rate]: " repro
read -p "[Intial infected]" intial



trap cleanUp 2

python3 simulation.py $popsize $vaccper $name $mortal $repro $intial
cat *.txt
