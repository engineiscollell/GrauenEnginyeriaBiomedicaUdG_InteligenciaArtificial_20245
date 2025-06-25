(define (domain laberint)
  (:requirements :strips :typing :fluents :negative-preconditions :conditional-effects :decrease)
  
  (:types 
    habitacio 
    passadis 
    clau 
    color
  )
  
  (:predicates
    ;; Connexió entre habitacions (no és simètric)
    (conecta ?pas - passadis ?hab1 - habitacio ?hab2 - habitacio)
    
    ;; Localització de Grimmy
    (es-troba ?hab - habitacio)
    
    ;; Estat del passadís
    (bloquejat ?pas - passadis ?col - color)
    (perillós ?pas - passadis)
    
    ;; Clau en una habitació
    (clau-a ?clau - clau ?hab - habitacio)
    
    ;; Clau portada per l'agent, amb el seu color associat
    (du ?clau - clau ?col - color)
    
    ;; Associació clau-color per obrir panys
    (obre ?clau - clau ?col - color)
    
    ;; Predicat auxiliar: indica que l’agent porta una clau (única)
    (porta-clau)
  )
  
  (:functions
    ;; Nombre d’usos restants de la clau
    (usos ?clau - clau)
  )
  
  ;;------------------------------------------------------------------
  ;; Accions
  ;;------------------------------------------------------------------
  
  ;; 1. Acció moure: mou l'agent d'una habitació a una altra si el passadís està obert.
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
      ;; Si el passadís és perillós, simulem que es col·lapsa (la connexió desapareix)
      (when (perillós ?pas)
        (not (conecta ?pas ?hab1 ?hab2))
      )
    )
  )
  
  ;; 2. Acció recollir: l'agent recull una clau de l'habitació si no porta cap clau.
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
  
  ;; 3. Acció deixar: l'agent deixa la clau que porta a l'habitació actual.
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
  
  ;; 4. Acció desbloquejar: l'agent desbloqueja un passadís bloquejat si porta la clau adequada.
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
      ;; Opcional: si (usos ?clau) arriba a 0, podríem eliminar (porta-clau)
      ;; (when (= (usos ?clau) 0)
      ;;   (not (porta-clau))
      ;; )
    )
  )
)

