(define (domain laberint-perillos)
  (:requirements :strips :typing :fluents :negative-preconditions :conditional-effects :decrease)
  
  (:types 
    habitacio 
    passadis 
    clau 
    color
  )
  
  (:predicates
    (conecta ?pas - passadis ?hab1 - habitacio ?hab2 - habitacio)
    (es-troba ?hab - habitacio)
    (bloquejat ?pas - passadis ?col - color)
    (perillós ?pas - passadis)
    (clau-a ?clau - clau ?hab - habitacio)
    (du ?clau - clau ?col - color)
    (obre ?clau - clau ?col - color)
    (porta-clau)
  )
  
  (:functions
    (usos ?clau - clau)
  )
  
  (:action moure
    :parameters (?hab1 - habitacio ?hab2 - habitacio ?pas - passadis ?col - color)
    :precondition (and
      (es-troba ?hab1)
      (conecta ?pas ?hab1 ?hab2)
      (not (bloquejat ?pas ?col))
    )
    :effect (and
      (not (es-troba ?hab1))
      (es-troba ?hab2)
      (when (perillós ?pas)
        (not (conecta ?pas ?hab1 ?hab2))
      )
    )
  )
  
  (:action recollir
    :parameters (?hab1 - habitacio ?clau - clau ?col - color)
    :precondition (and
      (es-troba ?hab1)
      (clau-a ?clau ?hab1)
      (obre ?clau ?col)
      (not (porta-clau))
    )
    :effect (and
      (du ?clau ?col)
      (not (clau-a ?clau ?hab1))
      (porta-clau)
    )
  )
  
  (:action deixar
    :parameters (?clau - clau ?hab1 - habitacio ?col - color)
    :precondition (and
      (du ?clau ?col)
      (es-troba ?hab1)
      (porta-clau)
    )
    :effect (and
      (not (du ?clau ?col))
      (clau-a ?clau ?hab1)
      (not (porta-clau))
    )
  )
  
  (:action desbloquejar
    :parameters (?pas - passadis ?col - color ?clau - clau ?hab1 - habitacio ?hab2 - habitacio)
    :precondition (and
      (es-troba ?hab1)
      (conecta ?pas ?hab1 ?hab2)
      (du ?clau ?col)
      (bloquejat ?pas ?col)
      (> (usos ?clau) 0)
    )
    :effect (and
      (not (bloquejat ?pas ?col))
      (decrease (usos ?clau) 1)
    )
  )
)

