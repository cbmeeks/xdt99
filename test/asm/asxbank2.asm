* SAVING BANKS

       SAVE >C000,>C020
       SAVE >D000,>D020
       SAVE >E000,>E020

       DATA >AFFE      * IGNORED

       AORG >C000,0
       DATA >C000
       DATA >C0FF

       AORG >C000,1
       DATA >C100
       DATA >C1FF

       AORG >C010
       DATA >CF00
       DATA >CFFF

       AORG >C018,1
       DATA >C118
       DATA >C1EE

       AORG >C018,0
       DATA >C018
       DATA >C0EE

       AORG >D008,0
       DATA >D008
       DATA >D0FF

       AORG >E018,1
       DATA >E108
       DATA >E1FF

       END
