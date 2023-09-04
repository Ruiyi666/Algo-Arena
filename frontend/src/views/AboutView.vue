<template>
  <main class="bg-base-200">
    <div class="container w-3/4 max-w-4xl px-4 py-16 mx-auto">
      <h1 class="mb-4 text-4xl font-bold">COSC349 Cloud Computing Architecture</h1>

      <div class="card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-3xl">Get Started</h2>
          <div class="p-4 rounded bg-base-200">
            <code>
          git clone https://github.com/Ruiyi666/COSC349.git
          <br>
          cd COSC349
          <br>
          vagrant up
                      </code>
          </div>
          <p>Navigate to <a href="http://192.168.56.11:80/" class="link link-primary">http://192.168.56.11:80/</a> or <a
              href="http://localhost:8080/" class="link link-primary">http://localhost:8080/</a></p>
        </div>
      </div>

      <div class="mt-6 card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-3xl">Description</h2>
          <p>
            <strong>Algo Arena</strong> is a gaming platform designed specifically for enthusiasts who enjoy strategy and
            coding. The platform facilitates an interactive environment where players can:
          </p>
          <ul class="pl-6 mb-4 list-disc">
            <li>Account Management - Register, log in, and manage profiles.</li>
            <li>Game Rooms - After logging in, players can enter a room using a room number, allowing them to engage in
              gameplay with other members of the same room.</li>
            <li>Future Prospects - In the pipeline is an exciting feature where users will have the ability to submit
              strategy codes. This will allow their in-game avatars or agents to move according to the predefined logic,
              making gameplay even more dynamic and strategy-driven.</li>
          </ul>

          <p>
            <strong>Algo Arena</strong> operates on three core virtual machines, each serving a distinct role:
          </p>
          <ul class="pl-6 list-decimal">
            <li><strong>192.168.56.11 - Frontend Server:</strong> This VM handles the user interface. Crafted with Vue.js,
              Tailwind CSS, and DaisyUI, it presents a responsive and intuitive gaming experience.</li>
            <li><strong>192.168.56.12 - Backend Server:</strong> The heart of our application logic. Developed using
              Django, it's responsible for game mechanics, user interactions, and real-time data processing. The
              integration of Django's RESTful API and Channels ensures seamless real-time communication.</li>
            <li><strong>192.168.56.13 - Database Server:</strong> The primary data repository for <strong>Algo
                Arena</strong>. All game replays, user profiles, and relevant data are stored here. It's compatible with
              both SQLite and MySQL, ensuring flexibility and security in data management.</li>
          </ul>
        </div>
      </div>

      <div class="mt-6 card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-3xl">Usage</h2>
          <h3 class="mb-2 text-2xl">Requirements</h3>
          <ul class="pl-6 list-disc">
            <li><a href="https://www.virtualbox.org/wiki/Download_Old_Builds_7_0" class="link link-primary">VirtualBox
                7.0.x</a></li>
            <li><a href="https://www.vagrantup.com/" class="link link-primary">Vagrant v2.3.7</a></li>
          </ul>

          <h3 class="mt-4 mb-2 text-2xl">Run</h3>
          <div class="p-4 rounded bg-base-200">
            <code>
          git clone https://github.com/ruiyi666/COSC349.git
          cd COSC349
          vagrant up
                      </code>
          </div>

          <h3 class="mt-4 mb-2 text-2xl">Cleanup</h3>
          <div class="p-4 rounded bg-base-200">
            <code>
          vagrant destroy
                      </code>
          </div>
        </div>
      </div>

      <div class="mt-6 card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-3xl">Database Description</h2>
          <p>
            The <strong>Algo Arena</strong> uses a relational database model, leveraging Django's ORM capabilities to
            manage and store game-related data. Here's an overview:
          </p>

          <h3 class="mb-2 text-2xl">Strategy Model</h3>
          <p>Represents a game strategy, containing:</p>
          <ul class="pl-6 list-disc">
            <li><strong>User:</strong> Foreign key link to the user who created the strategy.</li>
            <li><strong>Name:</strong> A name for the strategy.</li>
            <li><strong>Description:</strong> A detailed description of the strategy.</li>
            <li><strong>Is Manual:</strong> A boolean to determine if the strategy is manually controlled.</li>
            <li><strong>Timestamps:</strong> Track when the strategy was created and last updated.</li>
          </ul>

          <h3 class="mb-2 text-2xl">Game Model</h3>
          <p>Represents an individual game instance, containing:</p>
          <ul class="pl-6 list-disc">
            <li><strong>Timestamps:</strong> Track when the game was started and last updated.</li>
            <li><strong>Metadata:</strong> JSON field to store additional game-related data.</li>
          </ul>

          <h3 class="mb-2 text-2xl">Player Model</h3>
          <p>Represents a player in a game, containing:</p>
          <ul class="pl-6 list-disc">
            <li><strong>Game:</strong> Foreign key link to the game the player is participating in.</li>
            <li><strong>Strategy:</strong> Foreign key link to the strategy employed by the player.</li>
            <li><strong>Score:</strong> The player's score in the game.</li>
          </ul>

          <h3 class="mb-2 text-2xl">FrameAction Model</h3>
          <p>Stores actions performed by a player in a particular frame, containing:</p>
          <ul class="pl-6 list-disc">
            <li><strong>Player:</strong> Foreign key link to the player performing the action.</li>
            <li><strong>Frame:</strong> The specific frame number during which the action occurred.</li>
            <li><strong>Action:</strong> JSON field to detail the action taken.</li>
          </ul>

          <h3 class="mb-2 text-2xl">FrameState Model</h3>
          <p>Stores the state of a game at a particular frame, containing:</p>
          <ul class="pl-6 list-disc">
            <li><strong>Game:</strong> Foreign key link to the associated game.</li>
            <li><strong>Frame:</strong> The specific frame number.</li>
            <li><strong>State:</strong> JSON field detailing the game state at that frame.</li>
          </ul>

        </div>
      </div>

      <div class="mt-6 card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-3xl">Backend API</h2>
          <p>
            The backend of <strong>Algo Arena</strong> is designed to provide a robust, scalable, and efficient service
            for all game-related operations. The API is divided into two primary sets, the RESTful API for standard web
            operations and the WebSockets API for real-time communication.
          </p>

          <h3 class="mb-2 text-2xl">RESTful API</h3>
          <p>
            Our RESTful API uses the Django Rest Framework to create, read, update, and delete (CRUD) operations on our
            main entities.
          </p>
          <p><strong>Endpoints:</strong></p>
          <h3 class="mb-2 text-2xl">Endpoints</h3>

          <h4 class="mb-2 text-xl">Users</h4>
          <ul class="pl-6 list-disc">
            <li><strong>List, Create:</strong> /users/</li>
            <li><strong>Retrieve, Update, Delete:</strong> /users/{user_id}/</li>
          </ul>

          <h4 class="mb-2 text-xl">Strategies</h4>
          <ul class="pl-6 list-disc">
            <li><strong>List, Create:</strong> /strategies/</li>
            <li><strong>Retrieve, Update, Delete:</strong> /strategies/{strategy_id}/</li>
          </ul>

          <h4 class="mb-2 text-xl">Games</h4>
          <ul class="pl-6 list-disc">
            <li><strong>List, Create:</strong> /games/</li>
            <li><strong>Retrieve, Update, Delete:</strong> /games/{game_id}/</li>
          </ul>

          <h4 class="mb-2 text-xl">Players</h4>
          <ul class="pl-6 list-disc">
            <li><strong>List, Create:</strong> /games/{game_id}/players/</li>
            <li><strong>Retrieve, Update, Delete:</strong> /games/{game_id}/players/{player_id}/</li>
          </ul>

          <h4 class="mb-2 text-xl">Frame Actions</h4>
          <ul class="pl-6 list-disc">
            <li><strong>List, Create:</strong> /games/{game_id}/actions/</li>
            <li><strong>Retrieve, Update, Delete:</strong> /games/{game_id}/actions/{action_id}/</li>
          </ul>

          <h4 class="mb-2 text-xl">Frame States</h4>
          <ul class="pl-6 list-disc">
            <li><strong>List, Create:</strong> /games/{game_id}/states/</li>
            <li><strong>Retrieve, Update, Delete:</strong> /games/{game_id}/states/{state_id}/</li>
          </ul>


          <h3 class="mb-2 text-2xl">WebSocket API</h3>
          <p>
            For real-time communication, particularly during gameplay, <strong>Algo Arena</strong> leverages WebSockets.
          </p>
          <p><strong>Endpoints:</strong></p>
          <h3 class="mb-2 text-2xl">WebSocket API Endpoints</h3>

          <h4 class="mb-2 text-xl">Gameplay with Token Authentication</h4>
          <ul class="pl-6 list-disc">
            <li><strong>Endpoint:</strong> /ws/play/{room_id}/{token}/</li>
          </ul>

          <h4 class="mb-2 text-xl">General Gameplay</h4>
          <ul class="pl-6 list-disc">
            <li><strong>Endpoint:</strong> /ws/play/{room_id}/</li>
          </ul>


          <h3 class="mb-2 text-2xl">Exploring the API</h3>
          <p>
            Once you have your local environment set up and running:
          </p>
          <ol class="pl-6 list-decimal">
            <li>Navigate to <a href="http://localhost:8000/" class="link link-primary">http://localhost:8000/</a>.</li>
            <li>Here you'll find the browsable API provided by Django Rest Framework.</li>
            <li>You can explore various endpoints, see the data, and even test CRUD operations.</li>
          </ol>
        </div>
      </div>

      <div class="mt-6 card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-2xl">Frontend Features</h2>
          <p>Built with Vue.js, Tailwind CSS, and DaisyUI, the Algo Arena frontend offers the following features:</p>

          <ul class="pl-6 list-disc">
            <li><strong>Responsive Design:</strong> Ensures optimal viewing across various devices.</li>
            <li><strong>Main Routes:</strong>
              <ul class="pl-6 list-disc">
                <li>Home: The platform's entry point.</li>
                <li>Rankings: Displays player rankings.</li>
                <li>Game: The core gameplay interface.</li>
                <li>About: Information about the platform.</li>
                <li>404 Page: Handles undefined routes.</li>
              </ul>
            </li>
            <li><strong>State Management:</strong> Uses Vuex to manage user authentication and game state.</li>
            <li><strong>Icon Integration:</strong> Incorporates FontAwesome icons for a richer UI.</li>
            <li><strong>Global Components:</strong> A consistent header and footer across all views.</li>
            <li><strong>Navigation Guard:</strong> Middleware for route-specific logic.</li>
            <li><strong>Lazy Loading:</strong> Dynamic imports for efficient page loading.</li>
          </ul>

        </div>
      </div>

      <div class="mt-6 card bordered bg-base-100">
        <div class="card-body">
          <h2 class="mb-2 text-3xl">Future Plans</h2>
          <ul class="pl-6 list-disc">
            <li><strong>Programmatic Strategy:</strong> We aimed to integrate a feature where players can submit their own
              coded strategies. This would allow users to craft intelligent agents using programming logic, taking the
              gameplay to the next level. Players could challenge their own algorithms against others, fostering a
              competitive and learning environment.</li>
            <li><strong>Leaderboards:</strong> Introducing a system to rank players based on game performance and strategy
              effectiveness.</li>
          </ul>
        </div>
      </div>

    </div>
  </main>
</template>

<style scoped></style>
