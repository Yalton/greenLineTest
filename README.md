# greenLineTest 
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
  <a href="https://github.com/Yalton/greenLineTest">
    <img src="public/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">greenLineTest - Green Line test</h3>
  <p align="center">
    Web app designed to assign you a chad score based on the green line test
    <br />
    <a href="https://github.com/Yalton/greenLineTest"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Yalton/greenLineTest">View Demo</a>
    ·
    <a href="https://github.com/Yalton/greenLineTest/issues">Report Bug</a>
    ·
    <a href="https://github.com/Yalton/greenLineTest/issues">Request Feature</a>
  </p>
</div>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

Finally a mathematical representation of how Alpha/Beta the subjects of any photo are


This web app uses machine learning to perform a green line test and assign each person in the photo a "Chad Score" based on the slope of their lean

The app works well with images wherein both people are facing the camera and not overlapping too much with one and other

Offical Hosted Instance is available at [link](https://greenlinetest.billbert.co/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][python-badge]][python-url]
* [![TensorFlow][tensorflow-badge]][tensorflow-url]
* [![OpenCV][opencv-badge]][opencv-url]
* [![Node.js][nodejs-badge]][nodejs-url]
* [![Express.js][expressjs-badge]][expressjs-url]
* [![TypeScript][typescript-badge]][typescript-url]
* [![HTML5][html-badge]][html-url]
* [![CSS3][css-badge]][css-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
<!-- ## Getting Started

Clone the repository to your local system  -->

### Installation 

#### Node Endpoint

1. Clone the repo
   ```sh
   git clone https://github.com/Yalton/greenLineTest.git
   ```
2. Change this line in src/index.ts to whatever IP the Univorn endpoint will be running on 
   ```sh
   const fastApiRes = await axios.post('http://127.0.0.1:8000/predict', { base64_image });
   ```
3. Install nvm (Node Version Manager)
   ```sh
   curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
   ```
4. Install node version 17 
   ```
    nvm install 17
   ```
5. Use node version 17 
    ```
    nvm use 17
    ```
6. Install uuid and save-dev (Behaves weirdly so we do this seperate)
   ```
    npm install uuid
    npm install --save-dev @types/multer
   ```
7. Install NPM packages
   ```sh
   npm update
   ```
8. Build Typescript backend 
   ```
   npm run build
   ```
9. Start the server
   ```
    npm start
   ```

   
#### Univorn Endpoint

1. Clone the repo
   ```sh
   git clone https://github.com/Yalton/greenLineTest.git
   ```

2. Install OpenCV Dependencies
   ```sh
    apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx
    ```

3. Install packages from Univorn directory 
   ```sh
   pip3 install -r univorn/requirements.txt 
   ```
4. Run the Server (Within the Univorn directory)
   ```sh
   cd univorn
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```
#### Dockerized (Node)

Follow steps 1-6

7. Build the container
   ```
    docker compose build
   ```

8. Build the container
   ```
    docker compose up -d
   ```

#### Dockerized (Univorn)

1. Enter Univorn Directory
   ```
   cd univorn
   ```
2. Build the container
   ```
    docker compose build
   ```

3. Deploy the container
   ```
    docker compose up -d
   ```

Bare metal accesible @ localhost:3000

Dockerized Bare metal accesible @ localhost:3030

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Improve model which detects people (Dark colors and obscured figures confuse it currently)
- [ ] Add more features in general 

See the [open issues](https://github.com/Yalton/greenLineTest/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Dalton Bailey - [@yalt7117](https://twitter.com/yalt7117) - drbailey117@gmail.com

Project Link: [https://github.com/Yalton/greenLineTest](https://github.com/Yalton/greenLineTest)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* [InspirationRedditPost](https://www.reddit.com/r/KickStreaming/comments/14fv85p/how_you_can_download_kick_vods/) -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->


[tensorflow-badge]: https://img.shields.io/badge/Tensorflow-ffff00?style=for-the-badge&logo=tensorflow&logoColor=yellow
[tensorflow-url]: https://www.tensorflow.org/


[opencv-badge]: https://img.shields.io/badge/OpenCV-ff0000?style=for-the-badge&logo=opencv&logoColor=black
[opencv-url]: https://opencv.org/

[nodejs-badge]: https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white
[nodejs-url]: https://nodejs.org

[expressjs-badge]: https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white
[expressjs-url]: https://expressjs.com

[typescript-badge]: https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white
[typescript-url]: https://www.typescriptlang.org

[html-badge]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[html-url]: https://www.w3.org/html/

[css-badge]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[css-url]: https://www.w3.org/Style/CSS/Overview.en.html


[python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org
[contributors-shield]: https://img.shields.io/github/contributors/Yalton/greenLineTest.svg?style=for-the-badge
[contributors-url]: https://github.com/Yalton/greenLineTest/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Yalton/greenLineTest.svg?style=for-the-badge
[forks-url]: https://github.com/Yalton/greenLineTest/network/members
[stars-shield]: https://img.shields.io/github/stars/Yalton/greenLineTest.svg?style=for-the-badge
[stars-url]: https://github.com/Yalton/greenLineTest/stargazers
[issues-shield]: https://img.shields.io/github/issues/Yalton/greenLineTest.svg?style=for-the-badge
[issues-url]: https://github.com/Yalton/greenLineTest/issues
[license-shield]: https://img.shields.io/github/license/Yalton/greenLineTest.svg?style=for-the-badge
[license-url]: https://github.com/Yalton/greenLineTest/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/dalton-r-bailey
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 