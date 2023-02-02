# used to do integration testing 
# expectation: the state is not applied via salt_prometheus_exporter (since it uses salt state.highstate) under the hood
# and there might be changes to the client API where the test=True parameter is not evaluated correctly

# create an empty file
/tmp/test.file:
  file.touch