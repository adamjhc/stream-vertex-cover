# Stream

This directory serves as a example of how these algorithms would be more typically implemented into a streaming framework such as Kafka.

## Steps to run

1. `$ docker-compose up -d`
2. `$ python stream_producer.py worker -l info`
3. `$ python stream_kernel.py worker -l info`
4. `$ python stream_send.py request ..\test_sets\edge_lists\florentine_families.txt 6`
