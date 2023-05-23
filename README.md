cloudComputingEx1
cloud-based system to manage a parking lot, with the actions:

Entry (record time, license plate and parking lot)
Exit (return the charge for the time in the parking lot)
Price – 10$ per hour (by 15 minutes)
The system tracks cars entry & exit from parking lots, as well as computes their charge.
The system is deployed to AWS on an EC2 instance as standard application
written in python with Flask.

after cloning the repository:

install AWS CLI
configure AWS setup with access keys of an existing user and region: us-east-1
cd ./cloudComputing-hw1/
run the bash script that deploys the code to the cloud: ./setup.sh
you can see the script's output example at the file "output.txt".
you can send POSTs requests to the app's endpoints:

entry would return the ticket id of the entered car (with the requested parameters "plate" and "parkingLot").
after that, exit with the given ticket id would return the license plate, total parked time, the parking lot id and the charge (based on 15 minutes increments).
