
# Install
- sudo apt-get install espeak
- http://espeak.sourceforge.net/commands.html

# Usage
#### get voices:
```espeak --voices=en```

#### example
```espeak -v en-polish "text"```

#### set voice speed:
```espeak -s 175```

### Nice voice
```espeak -v en-scottish "Hello mister X, h
ow are you doing?"```

espeak -v en-scottish "Hello, how are you doing? I am doing fine."

espeak -v en+f3 -k5 -s150 "I've just picked up a fault in the AE35 unit"
espeak -v en+m3 -k5 -s150 "I've just picked up a fault in the AE35 unit"
