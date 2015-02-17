"""
Templates used to build hipchat api payloads
"""

host_template = """
<strong>{timestamp} - {hostname}  (nagios@{nagios_host})</strong><br/>
<strong>Type:</strong> {ntype}<br/>
<strong>Host:</strong> {hostname} (<a href="{hostaddress}">{hostaddress}</a>)<br/>
<strong>State:</strong> {state}<br>
<strong>Info:</strong>
<pre>{hostoutput}</pre>
"""

host_medium_template = "<strong>{timestamp} - {hostname} ({hostaddress}) - {ntype}/{state}</strong><br/><pre>{hostoutput}</pre>"
host_short_template = """[{ntype}] {hostname}: {hostoutput}"""

service_template = """
<strong>{timestamp} - {servicedesc} on {hostalias} (nagios@{nagios_host})</strong><br/>
<strong>Type:</strong> {ntype}<br/>
<strong>Host:</strong> {hostalias} (<a href="{hostaddress}">{hostaddress}</a>)<br/>
<strong>State:</strong> {state}<br/>
<strong>Info:</strong>
<pre>{serviceoutput}</pre>
"""

service_medium_template = "<strong>{timestamp} - {servicedesc} on {hostalias} ({hostaddress}) - {ntype}/{state}</strong><br/><pre>{serviceoutput}</pre>"
service_short_template = "[{ntype}] {hostalias} {servicedesc}: {serviceoutput}"


templates = {'host': host_template, 'medium-host': host_medium_template, 'short-host': host_short_template,
             'service': service_template, 'medium-service': service_medium_template, 'short-service': service_short_template}
