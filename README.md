# JobMatch
Developing System for Job Matching
This is a pyhton based project, whice use CVXOPT package , for implementaion of QP algorithm.
![JobMatch Logo](/static/app/images/JobMatch.JPG)

## Installation
Clone the repo, open a terminal, and install the dependencies: 
```
python -m pip install -r requirements.txt
```

## Motivation
Whether you are searching for yourself or searching others for your company, job finding can be tough, especially in the world of engineering. 
Thus, it can take a lot of time and resources to find one. 
This project,attempts to build a learning system that can filter most of the candidates using a set of questions with changeable weights, and only sending the companies the ones that answered the questions with a minimum grade.
To allow to the system to adapt according to the result of the candidates, the system will require the use of nonlinear-programming, and clusterization, in case there are different behaviors in a single company term of acceptance.
The system can save a lot of time and work both for the candidates and both for the companies.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)© JobMatch
