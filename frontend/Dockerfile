FROM node:current-stretch-slim

COPY . . 

# RUN /bin/bash -c mount --bind /maisie_node_modules /app/node_modules

RUN yarn global add create-react-app
RUN yarn global add react-scripts

RUN yarn install

EXPOSE 3000
CMD [ "yarn" "start" ]
# CMD [ "ls" "-a" ]