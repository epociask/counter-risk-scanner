# Risk Management Framework for Detecting Asset Related Counterparty Risks

## Counterparty Risk Enumeration
Counterparty risks qualitatively assess what party governs an asset and how they do so.

Ownership permissions over an asset could be considered risky under the following circumstances:

**A.** Priveleged token counterparty is able to unliterally modify contract state (i,e. revoke user funds, modify user funds) through superuser functions embed into the token implementation.

**B.** Priveleged counterparty is fully centralized as a single account able to unilaterally exercise malicious token priveleges. 

## Risk Identification Methodology
The outlined methodology:

1. Does the token contract have any unilateral superuser/counter-party controls?
2. Can these counterparty controls be exercised in a way that drastically impacts safe [custody](https://help.coinbase.com/en/coinbase/privacy-and-security/other/asset-security-review) of the asset?

3. How decentralized is a token counterparty?
* Is there at least greater than `(1/2n)` [trust](https://vitalik.ca/general/2020/08/20/trust.html) required for a counterparty group before priveleged functions can be called? 
* Is there at least greater than `x` actors total per some counterparty group?

**NOTE:** Understanding who governs a tokenized EVM asset would require mapping an Ethereum address to a real-human being. Unfortunatetly, this is not something that can be solved with a backend static analysis tool.

### Automation Assumption(s)
1. Tokenized asset inherits the _OpenZepellin_ `Ownable` standard [contract](https://docs.openzeppelin.com/contracts/3.x/api/access#Ownable) or the `AccessControl` standard [contract](https://docs.openzeppelin.com/contracts/3.x/api/access#AccessControl) for embedding access controls. 

2. Asset uses proxy/delegate upgrade pattern that is detectable by Etherscan compliant API _(Etherscan, Binance Scan)_.
