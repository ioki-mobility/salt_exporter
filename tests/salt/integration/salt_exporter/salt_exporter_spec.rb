require 'net/http'
require 'timeout'

control 'prometheus-salt-exporter' do
    title 'should be running & not applying the highstate'

    # Wait until metrics are available
    Timeout::timeout(90) {
        until (Net::HTTP.get_response(URI('http://localhost:9175/metrics')).body.include?("saltstack_nonhigh_states"))
            sleep(10)
        end
    }

    # Test metrics
    ## IPv4
    describe Net::HTTP.get_response(URI('http://127.0.0.1:9175/metrics')) do
        its(:code) { should eq '200' }
        its(:body) { should match 'saltstack_states_total{minion="minion1"} 1.0' }
        its(:body) { should match 'saltstack_error_states{minion="minion1"} 0.0' }
        its(:body) { should match 'saltstack_nonhigh_states{minion="minion1"} 1.0' }
        its(:body) { should match 'saltstack_highstate_error{minion="minion1"} 0.0' }
    end

    ## IPv6
    describe Net::HTTP.get_response(URI('http://[::1]:9175/metrics')) do
        its(:code) { should eq '200' }
        its(:body) { should match 'saltstack_states_total{minion="minion1"} 1.0' }
        its(:body) { should match 'saltstack_error_states{minion="minion1"} 0.0' }
        its(:body) { should match 'saltstack_nonhigh_states{minion="minion1"} 1.0' }
        its(:body) { should match 'saltstack_highstate_error{minion="minion1"} 0.0' }
    end

    # Test with salt cli
    describe command("salt '*' state.apply test=True") do
        its(:stdout) { should match 'Result: None' }
        its(:stdout) { should match 'File /tmp/test.file is set to be created' }
    end
end
