# kursach_23_02_01

the task: to develop a service for mailing list management, administration and statistics.

details: 
- Implement an interface for filling mailing lists, that is, a CRUD mechanism for managing mailing lists.
- Implement a mailing script that works both from the command line and on a schedule.
- Add configuration settings to run the task periodically.

The logic of the system
- After creating a new mailing list, if the current time is greater than the start time and less than the end time, all clients that are specified in the mailing list settings must be selected from the directory and sending is started for all these clients.
- If a mailing list is created with a start time in the future, the sending should start automatically after this time comes without additional actions from the system user.
- In the course of sending messages, statistics should be collected (see the description of the "message" and "attempt" entities above) for each message for subsequent reporting.
- An external service that receives sent messages can process a request for a long time, respond with incorrect data, or not accept requests at all for some time. Correct handling of such errors is needed. Problems with the external service should not affect the stability of the developed mailing service.

If you want to test just run two commands in different terminals:
 - python manage.py runserver
 - python manage.py runapscheduler  