# password-generator:
Generates a memorable (by pattern), strong (long and mixed characters) passwords.

# Install
`pip install password_gen`

# Documentation
`run(dictionary(optional), digit_range(optional), character_range(optional))`: Generates password
>`dictionary:{list} a list of preferred words`


>`digit_range:{list} a list specifying the range of digits. Ex [2, 8] -> digits from 2 to 7`


>`character_range:{list} a list specifying the range of ascii values of special characters. Ex [33, 36] -> '!, ~, #, $'`

# Usage
``` python
import password_gen as pg

print( pg.run() )

#  with parameters
print( pg.run(['willy', 'wonka', 'and', 'the', 'chocolate', 'factory'], [3, 8], [35, 38]))
# -> "the & wonka # choColate % willY"

# with some parameter
print( pg.run(None, None, [33, 35]) )
# -> "# Luxury 0 furnished 2 nIagarA 3 genEraTe !"
```
