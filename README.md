# OctoBot [2.0.12](https://github.com/Drakkar-Software/OctoBot/blob/master/CHANGELOG.md)
[![PyPI](https://img.shields.io/pypi/v/OctoBot.svg?logo=pypi)](https://pypi.org/project/OctoBot)
[![Downloads](https://pepy.tech/badge/octobot/month)](https://pepy.tech/project/octobot)
[![Dockerhub](https://img.shields.io/docker/pulls/drakkarsoftware/octobot.svg?logo=docker)](https://hub.docker.com/r/drakkarsoftware/octobot)
[![OctoBot-CI](https://github.com/Drakkar-Software/OctoBot/workflows/OctoBot-CI/badge.svg)](https://github.com/Drakkar-Software/OctoBot/actions)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Drakkar-Software/OctoBot)

#### Octobot Community
[![OctoBot](https://img.shields.io/badge/dynamic/json.svg?&url=https://octobot.cloud/api/community/stats&query=$.total_bots&color=blue&label=Installed%20OctoBots)]()
[![Telegram Chat](https://img.shields.io/badge/telegram-chat-green.svg?logo=telegram&label=Telegram)](https://t.me/octobot_trading)
[![Discord](https://img.shields.io/discord/530629985661222912.svg?logo=discord&label=Discord)](https://discord.com/invite/vHkcb8W)
[![Telegram News](https://img.shields.io/badge/telegram-news-blue.svg?logo=telegram&label=Telegram)](https://t.me/OctoBot_Project)
[![Twitter](https://img.shields.io/twitter/follow/DrakkarsOctobot.svg?label=twitter&style=social)](https://x.com/DrakkarsOctoBot)
[![YouTube](https://img.shields.io/youtube/channel/views/UC2YAaBeWY8y_Olqs79b_X8A?label=youtube&style=social)](https://www.youtube.com/@octobot1134)

<p align="center">
  <img src="../assets/illustration.png" alt="Octobot automating trades of its user while the user is relaxing on his couch">
</p>

<p align="center">
  <img src="../assets/ReadMeIntro.gif" alt="Introduction to OctoBot: choose a strategy, test it, use it and follow your gains" />
</p>

## What is Octobot  ?

[![OctoBot - Open Source Crypto Trading Bot Video](https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/meet_octobot_preview.png)](https://www.youtube.com/watch?v=TJUU62e1jR8)

[Octobot](https://www.octobot.cloud/trading-bot?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=readme_what_is_octobot) is a powerful open-source cryptocurrency trading robot.

OctoBot is highly customizable using its configuration and tentacles system.  
You can build your own bot using the infinite [configuration](https://www.octobot.cloud/en/guides/octobot-configuration/profile-configuration?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=configuration) possibilities such as  **technical analysis**, **social media processing** or even **external statistics management** like google trends.

Octobot's main feature is **evolution**, you can : 
- Create, backtest and optimize your unique trading strategy from scratch or using the existing [strategy bases](https://www.octobot.cloud/en/guides/octobot-trading-modes/trading-modes?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=strategy-bases).
- Use Technical indicator (TA), artificial intelligence, [ChatGPT predictions](https://www.octobot.cloud/en/blog/trading-using-chat-gpt?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=chatgpt), [TradingView automations](https://www.octobot.cloud/en/guides/octobot-interfaces/tradingview?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=trading-view) or [crypto baskets](https://octobot.cloud/features/crypto-basket?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=crypto-baskets) to automate your strategies.
- Trade any crypto on SPOT and Futures markets on more than [15 supported exchanges](https://www.octobot.cloud/en/guides/exchanges?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=exchanges).
- [Install](https://www.octobot.cloud/en/guides/octobot-advanced-usage/tentacle-manager?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=install_tentacles), [modify](https://www.octobot.cloud/en/guides/octobot-tentacles-development/create-a-tentacle?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=modify_tentacles) and even [create](https://www.octobot.cloud/en/guides/octobot-tentacles-development/create-a-tentacle?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=create_tentacles) new tentacles to build your ideal cryptocurrency trading robot.
- [Contribute](https://www.octobot.cloud/en/guides/octobot-developers-environment/setup-your-environment?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=contribute) to improve OctoBot core repositories and tentacles.

[OctoBot is AI ready](https://www.octobot.cloud/features/ai-trading-bot?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=ai-ready): Python being the main language for OctoBot, it's easy to integrate machine-learning libraries such as [Tensorflow](https://github.com/tensorflow/tensorflow) or any other libraries and take advantage of all the available data and create a very powerful trading strategy.

Looking for more info ? Check out our Octobot guides at [octobot.cloud/en/guides/octobot](https://www.octobot.cloud/en/guides/octobot?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=checkout_guides)

## Installation
### One click deployment using DigitalOcean
OctoBot can be easily launched on the cloud from the [DigitalOcean Marketplace](https://digitalocean.pxf.io/octobot-app).

[![Deploy on DO](https://mp-assets1.sfo2.digitaloceanspaces.com/deploy-to-do/do-btn-blue.svg)](https://digitalocean.pxf.io/start-octobot)

### Manual installations
To install OctoBot, you can either:
- [Deploy your OctoBot on the cloud using DigitalOcean](https://octobot.cloud/en/guides/octobot-installation/cloud-install-octobot-on-digitalocean?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=readme_deploy_on_cloud) and have your OctoBot automating your strategies 24/7.
- [Download and install](https://www.octobot.cloud/en/guides/octobot-installation/install-octobot-on-your-computer?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=readme_local_installation) OctoBot on your computer or server.
- Install OctoBot [using docker](https://www.octobot.cloud/en/guides/octobot-installation/install-octobot-with-docker-video?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=readme_docker_installation).
    Docker install in one line summary:
    ```
    docker run -itd --name OctoBot -p 80:5001 -v $(pwd)/user:/octobot/user -v $(pwd)/tentacles:/octobot/tentacles -v $(pwd)/logs:/octobot/logs drakkarsoftware/octobot:stable
    ```
    Your OctoBot will be accessible on [http://localhost](http://localhost).

## Exchanges
[![All OctoBot supported exchanges](../assets/exchange_logo.png)](https://www.octobot.cloud/en/guides/exchanges?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=binance)

Octobot supports many [exchanges](https://www.octobot.cloud/en/guides/exchanges?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=exchanges) thanks to the [ccxt library](https://github.com/ccxt/ccxt). 
To activate trading on an exchange, just configure OctoBot with your API keys as described [on the exchange setup guides](https://www.octobot.cloud/en/guides/octobot-configuration/exchanges?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=exchanges_setup_guides).


### Paper trading
To trade on any exchange, just activate the exchange in your OctoBot. This enables you to trade with [simulated money](https://www.octobot.cloud/en/guides/octobot-usage/simulator?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=paper-trading) on this exchange.

No exchange credential is required.

### Real trading
To use your real exchange account with OctoBot, enter your exchange API keys as described [on the exchange guides](https://www.octobot.cloud/en/guides/exchanges?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=exchanges_guides). 

## Follow your investments

You can follow your OctoBots portfolio, orders, trades and historical performance from your phone with our [Android application](https://play.google.com/store/apps/details?id=com.drakkarsoftware.octobotapp&utm_source=octobot-github&utm_media=readme&utm_content=mobile-app-link). You can also install the [web application](https://mobile.octobot.cloud/?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=follow_your_investments) to have the same experience on any smartphone or computer.

<p align="middle">
    <a href='https://apps.apple.com/us/app/octobot-crypto-investment/id6502774175?utm_source=octobot-github&utm_media=readme&utm_content=mobile-app-img'><img alt='Get it on the Apple Play Store' src='../assets/apple_store.png' height="50px"/></a>
    <a href='https://play.google.com/store/apps/details?id=com.drakkarsoftware.octobotapp&utm_source=octobot-github&utm_media=readme&utm_content=mobile-app-img'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png' height="50px"/></a>
</p>

<p align="middle">
  <a href="https://mobile.octobot.cloud/?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=follow_your_investments_image">
    <img src="../assets/mobile/bots-en.png" height="414" alt="Follow your bots from your mobile">
  </a>  
  &nbsp;&nbsp;&nbsp;&nbsp;    
  <a href="https://mobile.octobot.cloud/?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=follow_your_investments_image">
    <img src="../assets/mobile/bot-view-pf-en.png" height="414" alt="Follow each trade and profits of your OctoBot from your mobile">
  </a>  
</p>

## Testing trading strategies

OctoBot comes with its [built-in backtesting engine](https://www.octobot.cloud/en/guides/octobot-usage/backtesting?utm_source=github&utm_medium=dk&utm_campaign=regular_open_source_content&utm_content=backtesting) which enables you to trade with simulated money using historical exchange data.

[![Backtesting report using grid trading on eth btc with 8 percent profit](../assets/backtesting_report.jpg)](https://github.com/Drakkar-Software/OctoBot/blob/assets/backtesting_report.jpg)  

Backtesting will give you accurate insights on the past performance and behavior of trading strategies.

## Institutionals
If you are an institutional interested in a commercial license or custom development to suit your specific needs please contact us at <a href="mailto:contact@drakkar.software">contact@drakkar.software</a>. 

## Market making
A [market making distribution of OctoBot](https://github.com/Drakkar-Software/OctoBot-market-making) is available as a free open source software.

![octobot market making dashboard with buy and sell orders](https://raw.githubusercontent.com/Drakkar-Software/OctoBot-Market-Making/master/docs/octobot-market-making-dashboard-with-buy-and-sell-orders.png)

Advanced market making strategies can be automated on [market-making.octobot.cloud](https://market-making.octobot.cloud/), the self-service market making platform based on OctoBot. Feel free to contact us if you have any questions about it.

## Contribute from a browser IDE 
Make changes and contribute to OctoBot in a single click with an **already setup and ready to code developer environment** using Gitpod !

[![Contribute from Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Drakkar-Software/OctoBot)

## Hardware requirements  
- CPU : 1 Core / 1GHz  
- RAM : 250 MB  
- Disk : 1 GB

## Disclaimer
Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS 
AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. 

Always start by running a trading bot in simulation mode and do not engage money
before you understand how it works and what profit/loss you should expect.

Please feel free to read the source code and understand the mechanism of this bot.

## Sponsors
<table>
<tr>
<td>Thank you <a href="https://www.jetbrains.com" target="_blank">JetBrains</a> with PyCharm Pro for allowing us to develop the new features of OctoBot under the best conditions.</td>
<td><a href="https://www.jetbrains.com" target="_blank"><p align="center"><img src="https://resources.jetbrains.com/storage/products/pycharm/img/meta/pycharm_logo_300x300.png" width="100px"></p></a></td>
</tr>
<tr>
<td>Special thanks to <a href="https://www.chatwoot.com/" target="_blank">Chatwoot</a> for helping us assist the users of OctoBot.</td>
<td><a href="https://github.com/chatwoot/chatwoot" target="_blank"><p align="center"><img src="https://raw.githubusercontent.com/chatwoot/chatwoot/develop/public/brand-assets/logo.svg" width="500px"></p></a></td>
</tr>
<tr>
<td>Huge thank you to <a href="https://www.scaleway.com" target="_blank">Scaleway</a> for hosting OctoBot's cloud services.</td>
<td><a href="https://www.scaleway.com" target="_blank"><p align="center"><img src="https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/scaleway.svg" width="500px"></p></a></td>
</tr>
<tr>
<td>A big thank you to <a href="https://sentry.io/welcome/" target="_blank">Sentry</a> for helping us identify and understand errors in OctoBot to make it better.</td>
<td><a href="https://sentry.io/welcome/" target="_blank"><p align="center"><img src="https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/sentry.png" width="500px"></p></a></td>
</tr>
</table>

## License
GNU General Public License v3.0 or later.

See [GPL-3.0 LICENSE](https://github.com/Drakkar-Software/OctoBot/blob/master/LICENSE) to see the full text.
