# Notes for the Pairing Process

1. Button press to call init_pairing()

2. Start countdown, get return value from init_pairing() (True/False)
    - If true: Added module 
    - If false: Module not added, display error message
    
3. new_value_set()?
- 0 for off
- 1 for on
- new_value_set(module number, CHAR_ONOFF, value setting it to)

4. read_chars()?
    - Use this function in thread loop to continuously get values from the module?
    
    
    
# Pairing Interface

- Button for start pairing
- Pairing status (Currently pairing/Not currently pairing)


# Module Interface

Sensor

- Current value
- Set max threshold
- Set min threshold


On/Off

- Current status
- Turn on
- Turn off