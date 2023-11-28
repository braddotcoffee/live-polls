# 📊 Twitch Live Polls
Live poll that hooks into a Twitch channel to support live eval-bar view of infinite-duration polls 

![Live Poll Preview](static/LivePollPreview.mov)

## 🔍 Table of Contents
* [🚀 Quickstart](#🚀-quickstart)
* [🎡 Controlling Polls via Server Endpoints](#🎡-controlling-polls-via-server-endpoints)
* [👩‍💻 Contributing / Development Guide](#👩‍💻-contributing--development-guide)

## 🚀 Quickstart

Follow the steps below to run this project for your own Twitch Channel!

### Prerequisites
* Docker
* Docker Compose

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

## 👩‍💻 Contributing / Development Guide
Interested in contributing? Check out the [development guide](docs/CONTRIBUTING.md)!