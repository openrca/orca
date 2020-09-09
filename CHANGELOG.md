# Changelog

## [Unreleased](https://github.com/openrca/orca/tree/HEAD)

## [0.2.0](https://github.com/openrca/orca/tree/0.2.0) (2020-09-09)

[Full Changelog](https://github.com/openrca/orca/compare/0.1.0...0.2.0)

**Implemented enhancements:**

- Add alerts API [\#98](https://github.com/openrca/orca/issues/98)
- Add node properties to graph payload [\#96](https://github.com/openrca/orca/issues/96)
- Add CORS headers to API [\#94](https://github.com/openrca/orca/issues/94)
- Add API for retrieving graph state by datetime [\#92](https://github.com/openrca/orca/issues/92)
- Add sample values for Istio operator [\#67](https://github.com/openrca/orca/issues/67)
- Remove alert if resolved in upstream [\#63](https://github.com/openrca/orca/issues/63)
- Change logo [\#60](https://github.com/openrca/orca/issues/60)
- Falco alerts mapping [\#35](https://github.com/openrca/orca/issues/35)
- Prometheus alerts mapping [\#34](https://github.com/openrca/orca/issues/34)
- Add probe for Kubernetes ingress [\#28](https://github.com/openrca/orca/issues/28)
- Add probe for Kubernetes cron jobs [\#27](https://github.com/openrca/orca/issues/27)
- Add probe for Kubernetes jobs [\#26](https://github.com/openrca/orca/issues/26)
- Add Helm chart for UI [\#88](https://github.com/openrca/orca/pull/88) ([bzurkowski](https://github.com/bzurkowski))

**Fixed bugs:**

- Restart watch on K8S 410 gone instead of restarting the probe [\#81](https://github.com/openrca/orca/issues/81)
- Invalid origin for Gateway entities in Istio linker [\#80](https://github.com/openrca/orca/issues/80)
- Alert nodes not linked in the graph [\#71](https://github.com/openrca/orca/issues/71)
- Unable to enable Prometheus probe [\#69](https://github.com/openrca/orca/issues/69)
- Unify extraction of alert message in Prometheus probe [\#66](https://github.com/openrca/orca/issues/66)
- Deleted nodes not excluded from query result [\#51](https://github.com/openrca/orca/issues/51)
- Empty Kubernetes fields in Falco output [\#13](https://github.com/openrca/orca/issues/13)

**Closed issues:**

- Add information about Helm version support [\#90](https://github.com/openrca/orca/issues/90)

**Merged pull requests:**

- Remove alert if if status is down [\#102](https://github.com/openrca/orca/pull/102) ([bzurkowski](https://github.com/bzurkowski))
- Graph filtering by point in time [\#100](https://github.com/openrca/orca/pull/100) ([bzurkowski](https://github.com/bzurkowski))
- Add alerts endpoint [\#99](https://github.com/openrca/orca/pull/99) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Add extended graph node payload [\#97](https://github.com/openrca/orca/pull/97) ([bzurkowski](https://github.com/bzurkowski))
- Add CORS headers to API [\#95](https://github.com/openrca/orca/pull/95) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Add information about Helm version support [\#91](https://github.com/openrca/orca/pull/91) ([bzurkowski](https://github.com/bzurkowski))
- Add alert probe for Zabbix [\#85](https://github.com/openrca/orca/pull/85) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Break instead of return from K8S watch loop [\#84](https://github.com/openrca/orca/pull/84) ([bzurkowski](https://github.com/bzurkowski))
- Fix Gateway origin in Istio linker [\#83](https://github.com/openrca/orca/pull/83) ([bzurkowski](https://github.com/bzurkowski))
- Update logo [\#79](https://github.com/openrca/orca/pull/79) ([filwie](https://github.com/filwie))
- Add probe for Kubernetes ingress [\#78](https://github.com/openrca/orca/pull/78) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Add probe for Kubernetes cron\_jobs [\#77](https://github.com/openrca/orca/pull/77) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Add probe for Kubernetes jobs [\#76](https://github.com/openrca/orca/pull/76) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Add more fields for alert message extraction [\#73](https://github.com/openrca/orca/pull/73) ([bzurkowski](https://github.com/bzurkowski))
- Fix alert linker [\#72](https://github.com/openrca/orca/pull/72) ([bzurkowski](https://github.com/bzurkowski))
- Fix Prometheus enablement flag [\#70](https://github.com/openrca/orca/pull/70) ([bzurkowski](https://github.com/bzurkowski))
- Add sample values for Istio operator [\#68](https://github.com/openrca/orca/pull/68) ([bzurkowski](https://github.com/bzurkowski))
- Convert README to markdown [\#61](https://github.com/openrca/orca/pull/61) ([bzurkowski](https://github.com/bzurkowski))
- Falco alerts mapping [\#59](https://github.com/openrca/orca/pull/59) ([aleksandra-galara](https://github.com/aleksandra-galara))
- Complete mapping of Prometheus alerts [\#53](https://github.com/openrca/orca/pull/53) ([aleksandra-galara](https://github.com/aleksandra-galara))

## [0.1.0](https://github.com/openrca/orca/tree/0.1.0) (2020-04-17)

[Full Changelog](https://github.com/openrca/orca/compare/7949332e2d0f75a6e15ecb2fc2d7cf9aa67af6bd...0.1.0)

**Implemented enhancements:**

- Improve concurrency model [\#16](https://github.com/openrca/orca/issues/16)
- Add ArangoDB graph backend [\#12](https://github.com/openrca/orca/issues/12)
- Add time signatures to graph nodes [\#11](https://github.com/openrca/orca/issues/11)
- Add contribution guide [\#10](https://github.com/openrca/orca/issues/10)
- Separate upstream IDs from IDs managed by graph DB [\#54](https://github.com/openrca/orca/pull/54) ([bzurkowski](https://github.com/bzurkowski))
- Parametrize Helm chart [\#46](https://github.com/openrca/orca/pull/46) ([bzurkowski](https://github.com/bzurkowski))
- Configurable probe enablement [\#45](https://github.com/openrca/orca/pull/45) ([bzurkowski](https://github.com/bzurkowski))
- Remove Neo4j graph backend [\#43](https://github.com/openrca/orca/pull/43) ([bzurkowski](https://github.com/bzurkowski))
- Add time to graph elements [\#41](https://github.com/openrca/orca/pull/41) ([bzurkowski](https://github.com/bzurkowski))
- Handle Kubernetes watch errors [\#40](https://github.com/openrca/orca/pull/40) ([bzurkowski](https://github.com/bzurkowski))
- Implement generic ingestor setup [\#21](https://github.com/openrca/orca/pull/21) ([bzurkowski](https://github.com/bzurkowski))
- Add graph lock [\#19](https://github.com/openrca/orca/pull/19) ([bzurkowski](https://github.com/bzurkowski))
- Add ArangoDB graph backend [\#6](https://github.com/openrca/orca/pull/6) ([bzurkowski](https://github.com/bzurkowski))
- Add generic push probe [\#5](https://github.com/openrca/orca/pull/5) ([bzurkowski](https://github.com/bzurkowski))
- Add resync period option for probes [\#4](https://github.com/openrca/orca/pull/4) ([bzurkowski](https://github.com/bzurkowski))
- Add code of conduct and changelog [\#3](https://github.com/openrca/orca/pull/3) ([bzurkowski](https://github.com/bzurkowski))
- Add Graph API [\#2](https://github.com/openrca/orca/pull/2) ([bzurkowski](https://github.com/bzurkowski))
- Add config module [\#1](https://github.com/openrca/orca/pull/1) ([bzurkowski](https://github.com/bzurkowski))

**Fixed bugs:**

- Falco unable to start: "error opening device /host/dev/falco0" [\#55](https://github.com/openrca/orca/issues/55)
- Failed to perform API request to Prometheus [\#38](https://github.com/openrca/orca/issues/38)
- Cannot log into noe4j [\#36](https://github.com/openrca/orca/issues/36)
- Neo4j: Failed to read from defunct connection [\#32](https://github.com/openrca/orca/issues/32)
- Istio watches fail periodically [\#18](https://github.com/openrca/orca/issues/18)
- Filter out soft-deleted elements in graph operations [\#57](https://github.com/openrca/orca/pull/57) ([bzurkowski](https://github.com/bzurkowski))
- Fix non-deterministic link source-target ordering [\#56](https://github.com/openrca/orca/pull/56) ([bzurkowski](https://github.com/bzurkowski))

**Merged pull requests:**

- Add contribution guide [\#33](https://github.com/openrca/orca/pull/33) ([bzurkowski](https://github.com/bzurkowski))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
