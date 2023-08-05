def d(config):
    """
    Read channels on modbus device, scale and calibrate the values, and store teh data in a MySQL database.
    The inputs are provided by a configuration dictonary that describe general information for
    data aquistion and the devices.
    
    Parameters
    ----------
    :config : dictionary
        Configuration options, see :ref:`devicetoclient_config`
    """ 
    
    return 2