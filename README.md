<p align="center">
  <img src="static/TwitchPolls.png">
  <b>Infinite Duration Twitch Polls with Eval Bar Overlay</b>
</p>
<h4 align="center">
<a href="#quickstart">🚀 Quickstart</a> |
<a href="#voting-configuration">🗳️ Voting Configuration</a> |
<a href="#endpoints">🎡 Controlling Polls</a> |
<a href="#contributing">👩‍💻 Contributing </a>
</h4>

https://github.com/braddotcoffee/live-polls/assets/17772186/3ce95b26-6a4a-416d-abe0-6e34bea65029

<a id="quickstart"></a>

## 🚀 Quickstart

Follow the steps below to run this project for your own Twitch Channel!

### Prerequisites

- Docker
- Docker Compose

### Backend Setup

Copy the example config into a `config-prod.yaml` for use with the production Docker Compose configuration

```bash
cd backend
cp config-example.yaml config-prod.yaml
```

**Edit the example config to point to your Twitch channel.** This can be found under `Voting > ChannelName`.

Copy the example secrets file into `secrets-prod.yaml` for use with the production Docker Compose configuration

```bash
cp secrets-example.yaml secrets-prod.yaml
```

**Edit the file to include a LONG and RANDOM token for authenticating to your server endpoints**. This can be found under `Server > Token`.

Spin up the Docker Compose. The service will now be listening on `localhost:3005`.

```bash
docker compose -f compose-prod.yaml up -d
```

### Frontend Setup

Create a .env file that points at your backend for the `NEXT_PUBLIC_API_URL`

```bash
cd ..
cd frontend
echo 'NEXT_PUBLIC_API_URL="localhost:3005"' > .env
```

Build the frontend for production and start it up. The app will be served on `localhost:3000`.

```bash
npm run build
npm start
```

<a id="voting-configuration"></a>

## 🗳️ Voting Configuration

Voting takes place by sending a message in Twitch Chat that corresponds to a configured `PositiveKeyword` or `NegativeKeyword`. These can be configured in your `config.yaml`:

```yaml
Voting:
  PositiveKeyword:
  NegativeKeyword:
```

Messages that match these keywords exactly (case-insensitive) will be counted as votes.

```
"voteKeyword" <- Counted as Vote
"Message that contains voteKeyword" <- Not counted as Vote
```

### SingleVotePerUser Mode

By default, the application only allows one vote per user, **but allows them to change it at any time**. If you wish to disallow changing of votes, consider using the built-in Twitch polls functionality (these have a maximum duration of 10 minutes).

SingleVotePerUser Mode can be enabled in the `config.yaml`

```yaml
Voting:
  SingleVotePerUser: True
```

### MultipleVotePerUser Mode

MultipleVotePerUser mode allows users to vote as many times as they want throughout the duration of the poll. This encourages users to spam chat for constant engagement if you want your chat to fly by!

MultipleVotePerUser Mode can be enabled in the `config.yaml`

```yaml
Voting:
  SingleVotePerUser: False
```

<a id="endpoints"></a>

## 🎡 Controlling Polls via Server Endpoints

### Reset Poll

Reset a poll to 0 votes and an entirely neutral bar

```bash
curl --request GET \
  --url localhost:3005/reset \
  --header 'x-access-token: YOUR_ACCESS_TOKEN'
```

### Stop Poll

Stop poll from accepting votes

```bash
curl --request GET \
  --url localhost:3005/stop \
  --header 'x-access-token: YOUR_ACCESS_TOKEN'
```

### Start Poll

Start poll so that it may accept votes. **NOTE:** This does not reset the poll.

```bash
curl --request GET \
  --url localhost:3005/start \
  --header 'x-access-token: YOUR_ACCESS_TOKEN'
```

<a id="contributing"></a>

## 👩‍💻 Contributing / Development Guide

Interested in contributing? Check out the [development guide](docs/CONTRIBUTING.md)!
