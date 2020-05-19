(ns gridworld
  ;; Used to make matrix math easier
  (:require [clojure.core.matrix :as m]))

;; Given a number, x, returns x to the power of n
(defn ** [x n]
  "x to the power of n."
  (reduce * (repeat n x)))

;; The necessary constants that are used throughout the program
(def greedy 0.98)
(def discount 0.9)
(def total-reward 0)
(def current-movement "None")


;; Used to reset the states-and-actions to a blank array
(defn restart-sabr []
  "Restarts states-and-actions."
  (def states-and-actions []))

;; The restart function, used right before starting a new run
(defn restart []
  "Restarts the game state."
  ;; Both the states and value-functions are a 4 x 4 matrix for each of the grid positions with the third dimension being used for one of the 4 possible move directions.
  (def states (m/new-array [4 4 4]))
  (def value-functions (m/new-array [4 4 4]))
  ;; The robot starts in grid position (2,2)
  (def robot-position [2 2])
  ;; The total reward over the run
  (def total-reward 0)
  (restart-sabr))

;; Given the move direction, it adds its current position on the grid and move direction to the total list of states and actions.
(defn sabr [move]
  "Updates the states and actions list."
  (def states-and-actions (conj states-and-actions (conj robot-position move)))
  (println states-and-actions))

;; The reward function rewards the agent for its actions.
(defn reward-fn [reward]
  "Given a set reward, gives it to the agent for all previous moves."
  (println (count states-and-actions))
  ;; Loop for as many different states-and-actions there are.
  (dotimes [num (count states-and-actions)]
    (println "Number: " num)
    ;; Gets the current states-and-actions index
    (let* [indexes (get states-and-actions num)]
      (println "Indexes: " indexes)
      ;; Updates the value-functions with matrix set, given its three indexes it adds the current value to
      ;; the reward times the discount to the power of the current index number.
      (def value-functions (m/mset value-functions (first indexes) (second indexes) (nth indexes 2)
                                   (+ (m/mget value-functions (first indexes) (second indexes) (nth indexes 2))
                                      (* reward (** discount num)))))))
  ;; Restart the states and actions so it can accumulate for the next reward.
  (restart-sabr))

;; Give a negative reward for staying in the same position
(defn same-position []
  "Gives a penalty for staying in the same position."
  (def total-reward (dec total-reward))
  (def current-movement "None"))

;; Gives a detriment for moving off of gridworld
(defn move-off-grid [movement]
  "Off grid movement results in a negative reward and being in the same position."
  (def current-movement "Move")
  (when (and (= (first robot-position) 0) (= movement "w"))
    (same-position)
    (reward-fn -1))
  (when (and (= (first robot-position) 3) (= movement "e"))
    (same-position)
    (reward-fn -1))
  (when (and (= (second robot-position) 0) (= movement "n"))
    (same-position)
    (reward-fn -1))
  (when (and (= (second robot-position) 3) (= movement "s"))
    (same-position)
    (reward-fn -1)))

;; Used to move the robots position and updates the robot-position array
(defn move-robot [x-or-y amount]
  "Takes in either a 0 or 1 for x-or-y and 1 or -1 for movement"
  ;; Gets the element representing the x or y axis then adds its latest movement to its last position
  (def robot-position (assoc robot-position x-or-y (+ (nth robot-position x-or-y) amount))))

;; The reward and jump function rolled into one, as long as it is in the correct position.
(defn jump []
  "Used to give the only positive reward upon succesful navigation."
  ;; When the robot is in grid position (1,0)
  (when (and (= (first robot-position) 1) (= (second robot-position) 0))
    (def current-movement "Jumped")
    (def total-reward (inc total-reward))
    ;; Moves it to its new location on gridworld
    (def robot-position [1 3])
    (reward-fn 10)))

;; (defn update-states [direction]
;;   (def states (m/mset states (first robot-position)
;;                       (second robot-position)
;;                       direction
;;                       (inc (m/mget states (first robot-position) (second robot-position) direction)))))

;; Updates the states count with how many times it has been in that position and done that move.
(defn update-states [direction]
  "Update states count"
  ;; Adds to the states and actions list
  (sabr direction)
  ;; Updates the states variable by one starting at 0 for never been in that position before.
  (def states (m/mset states (first robot-position)
                      (second robot-position)
                      direction
                      (inc (m/mget states (first robot-position) (second robot-position) direction)))))

;; Depending on what direction the robot moves, update that position-move
(defn movement [movement]
  "Gives a number to each direction."
  (cond
    (= movement "n") (update-states 0)
    (= movement "e") (update-states 1)
    (= movement "s") (update-states 2)
    (= movement "w") (update-states 3))

  ;; Checks to see if it moves off the grid
  (move-off-grid movement)
  ;; As long as it does not move off the grid, move the robot
  (when (not (= current-movement "None"))
    (def current-movement "Yes")
    (cond
      (= movement "w") (move-robot 0 -1)
      (= movement "e") (move-robot 0 1)
      (= movement "n") (move-robot 1 -1)
      (= movement "s") (move-robot 1 1))
    ;; Else check if it should jump
    (jump)))

;; Used to display the current gridworld
(defn display-gridworld []
  "Prints the current gridworld layout to terminal."
  (dotimes [y 4]
    (dotimes [x 4]
      (if (and (= (first robot-position) x) (= (second robot-position) y))
        (print "|R")
        (print "| ")))
    (print "|")
    (println)))

;; Gets the maximum value and value position given an array.
(defn get-max-pos [array]
  "Get the max value along with its position"
  ;; Start with getting the absolute minimum value in the array, and minus 10 for good measure.
  (def maximum (- (apply min array) 10))
  (def max-index -1)
  (dotimes [i (count array)]
    (when (> (get array i) maximum)
      (def maximum (get array i))
      (def max-index i)))
  ;; Returns the maximum and its position.
  (list maximum max-index))

;; The greedy move, or in other words the move that is most likely going to give the best reward.
(defn greedy-move []
  "Be greedy for the reward"
  ;; Get the maximum possible direction to move in, given the value function
  (let [choices (m/mget value-functions (first robot-position) (second robot-position))
        max-index (second (get-max-pos choices))]
    (println choices)
    (println (get-max-pos choices))
    (cond
      (= 0 max-index) "n"
      (= 1 max-index) "e"
      (= 2 max-index) "s"
      (= 3 max-index) "w")))

;; Used to display at the end the best possible move the agent could take from each gridworld square.
(defn display-best []
  "Display the best possible move."
  (dotimes [y 4]
    (dotimes [x 4]
      (let [choices (m/mget value-functions x y)
            max-index (second (get-max-pos choices))]
        (cond
          (= 0 max-index) (print "N")
          (= 1 max-index) (print "E")
          (= 2 max-index) (print "S")
          (= 3 max-index) (print "W"))))
    (println)))

(defn play [mov]
  "Does the right movement"
  (movement mov))
  ;; (display-gridworld))

;; The main function responsible for the gamestate parameters
(defn -main []
  "The main function"
  ;; Restart the variables
  (restart)
  (println "Starting...")
  ;; Define the number tasks per episode
  (def number-of-tasks 100000)
  (dotimes [number-of-episodes 1]
    (dotimes [count number-of-tasks]
      ;; Given a random number between 0 and 1, if the greedy percent is greater than the number, do a greedy move.
      (if (> greedy (rand 1))
        (play (greedy-move))
        ;; Else do an exploratory move.
        (play (rand-nth ["n" "e" "s" "w"])))))
  (println "Total Reward: " total-reward)
  (def final-states (m/div states number-of-tasks))
  (println value-functions))
