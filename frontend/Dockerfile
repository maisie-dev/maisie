FROM node:12.6.0-stretch-slim

COPY . . 

RUN yarn global add create-react-app
RUN yarn global add react-scripts

RUN yarn install

EXPOSE 3000
CMD [ "yarn" "start" ]
