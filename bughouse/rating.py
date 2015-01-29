K <- 10

WIN_SELF <- 55 / K 
WIN_PARTNER <-  45 / K
LOSE_SELF <- - WIN_SELF 
LOSE_PARTNER <- - WIN_PARTNER 

PARTNER_WEIGHT <- 1/3
SELF_WEIGHT <- 1 - PARTNER_WEIGHT

win_probability_from_rating <- function(r1, r2){
  diff <- r1 - r2
  1 / ( 10^( diff / 400) +1)
}

weighted_rating <- function(self_rating, partner_rating, self_weight = SELF_WEIGHT, partner_weight = PARTNER_WEIGHT){
  (self_rating * self_weight) + (partner_rating * partner_weight) 
}

points_from_probability <- function(probability_to_win, victory_condition_constant){
  (1 - probability_to_win) * victory_condition_constant
}

compute_changes <- function}(r_winner, r_winner_p, r_loser, r_loser_partner){
  w1_weighted <- weighted_rating(r_winner_p, r_winner)
  w2_weighted <- weighted_rating( r_winner,r_winner_p)
  l1_weighted <- weighted_rating(r_loser_partner, r_loser)
  l2_weighted <- weighted_rating(r_loser, r_loser_partner)

  w1_points <- points_from_probability(win_probability_from_rating(l1_weighted, w1_weighted), WIN_SELF)
  w2_points <- points_from_probability(win_probability_from_rating(l2_weighted, w2_weighted), WIN_PARTNER )
  l1_points <- points_from_probability(1 - win_probability_from_rating(w1_weighted, l1_weighted), LOSE_SELF)
  l2_points <- points_from_probability(1 - win_probability_from_rating(w2_weighted, l2_weighted), LOSE_PARTNER)

  c(w1_points, w2_points, l1_points, l2_points)





