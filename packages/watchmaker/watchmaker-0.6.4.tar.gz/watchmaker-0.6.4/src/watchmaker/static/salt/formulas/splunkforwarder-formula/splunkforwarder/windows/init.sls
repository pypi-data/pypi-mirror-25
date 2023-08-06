{%- from tpldir ~ '/map.jinja' import splunkforwarder with context %}

splunkforwarder-install:
  pkg.installed:
    - name: {{ splunkforwarder.package }}
    - allow_updates: True
    - require_in:
      - file: splunkforwarder-deploymentclient.conf
      - file: splunkforwarder-log-local.cfg
    - onchanges_in:
      - service: splunkforwarder-service-stop
      - cmd: splunkforwarder-clone-prep-clear-config

splunkforwarder-deploymentclient.conf:
  file.managed:
    - name: {{ splunkforwarder.deploymentclient.conf }}
    - contents: |
        [deployment-client]
        disabled = false
        clientName = {{ splunkforwarder.deploymentclient.client_name }}

        [target-broker:deploymentServer]
        targetUri = {{ splunkforwarder.deploymentclient.target_uri }}
    - makedirs: True
    - watch_in:
      - service: splunkforwarder-service-start

splunkforwarder-log-local.cfg:
  file.managed:
    - name: {{ splunkforwarder.log_local.conf }}
    - contents: |
        {{ splunkforwarder.log_local.contents | indent(8) }}
    - makedirs: True
    - watch_in:
      - service: splunkforwarder-service-start

splunkforwarder-service-stop:
  service.dead:
    - name: {{ splunkforwarder.service }}
    - require_in:
      - cmd: splunkforwarder-clone-prep-clear-config

splunkforwarder-clone-prep-clear-config:
  cmd.run:
    - name: '"{{ splunkforwarder.bin_file }}" clone-prep-clear-config || exit /B 0'
    - watch_in:
      - service: splunkforwarder-service-start

splunkforwarder-service-start:
  service.running:
    - name: {{ splunkforwarder.service }}
