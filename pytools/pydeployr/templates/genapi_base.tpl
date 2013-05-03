[program:{{genapi_api_id}}]
command={{python_interpreter}} {{genapi_start}} --logging={{logging_level}} --riak_host={{riak_host}} --riak_pb_port={{riak_port}} --port={{app_port}} --api_id={{genapi_api_id}} --api_version={{genapi_version}} --env={{genapi_env}} --entity={{genapi_entity_list}} --api_key={{genapi_api_key}}
directory={{genapi_home_directory}}
user={{genapi_user}}
autorestart=true
redirect_stderr=true
stdout_logfile={{genapi_log_file}}
loglevel=info
