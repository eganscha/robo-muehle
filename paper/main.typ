#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [Robo Arm],
  paper-size: "a4",
  abstract: [This work presents a robotic system capable of autonomously playing Nine Men’s Morris by integrating computer vision and strategic decision-making. The system employs a robotic manipulator to physically move pieces on the board while leveraging YOLO-based visual perception to detect the current board state in real time. A custom-trained model evaluates the game state and selects optimal moves, enabling the robot to play strategically against human or simulated opponents. We detail the design of the perception pipeline, the interfacing of the robot arm with the board, and the training of the game model, emphasizing how these components interact to achieve seamless gameplay.],
  authors: (
    (
      name: "Frederik Schwarz",
      department: [Informatik],
      organization: [Hof-University],
    ),
  ),
  bibliography: bibliography("refs.bib"),
)
#pagebreak()
#include "ai.typ"
