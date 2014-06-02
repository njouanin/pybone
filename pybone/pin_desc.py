BBB_control_module_addr=0x44e10000

############################################################################
# P8 header definition
# 
# Each array element contains :
#   - head_pin : Pin number on P8 header
#   - head_name : Pin name on P8 header (see SRM, table 11, column NAME)
#   - proc_pin : corresponding processor pin (See AM3358 datasheet)
#   - reg_offet : pin control module register offset
#   - driver_pin : pin number see from linux pinctrl-single driver
#   - proc_pin_name : processor pin name (see table 2-7 of AM3358 datasheet)
#   - signal_name : name of muxed signal (7 modes)
#   - reset_mode : mode set by default on processor reset
#   - gpio_chip : GPIO chip number, n in GPIOn_m
#   - gpio_number : GPIO number, gpio_number = 32*n+m with GPIOn_m
#   - notes
#
############################################################################
BBB_P8_DEF = [
    {
        'head_pin':1,
        'head_name': 'GND', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'GND'
    },
    {
        'head_pin':2,
        'head_name': 'GND', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None, 
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'GND'
    },
    {
        'head_pin':3,
        'head_name': 'GPIO1_6', 
        'proc_pin': 'R9', 
        'reg_offset': 0x818, 
        'driver_pin': 6, 
        'proc_pin_name': 'GPMC_AD6', 
        'proc_signal_name': ['gpmc_ad6', 'mmc1_dat6', None, None, None, None, None, 'gpio1_6'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 38,
        'notes': None
    },
    {
        'head_pin':4,
        'head_name': 'GPIO1_7', 
        'proc_pin': 'T9', 
        'reg_offset': 0x81c, 
        'driver_pin': 7, 
        'proc_pin_name': 'GPMC_AD7', 
        'proc_signal_name': ['gpmc_ad7', 'mmc1_dat7', None, None, None, None, None, 'gpio1_7'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 39,
        'notes': None
    },
    {
        'head_pin':5,
        'head_name': 'GPIO1_2', 
        'proc_pin': 'R8', 
        'reg_offset': 0x808, 
        'driver_pin': 2, 
        'proc_pin_name': 'GPMC_AD2', 
        'proc_signal_name': ['gpmc_ad2', 'mmc1_dat2', None, None, None, None, None, 'gpio1_2'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 34,
        'notes': None
    },
    {
        'head_pin':6,
        'head_name': 'GPIO1_3', 
        'proc_pin': 'T8', 
        'reg_offset': 0x80c, 
        'driver_pin': 3, 
        'proc_pin_name': 'GPMC_AD3', 
        'proc_signal_name': ['gpmc_ad3', 'mmc1_dat3', None, None, None, None, None, 'gpio1_3'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 35,
        'notes': None
    },
    {
        'head_pin':7,
        'head_name': 'TIMER4', 
        'proc_pin': 'R7', 
        'reg_offset': 0x890, 
        'driver_pin': 36, 
        'proc_pin_name': 'GPMC_ADVn_ALE',
        'proc_signal_name': ['gpmc_advn_ale', None, 'timer4', None, None, None, None, 'gpio2_2'], 
        'reset_mode': 7, 
        'gpio_chip': 2,
        'gpio_number': 66,
        'notes': None
    },
    {
        'head_pin':8,
        'head_name': 'TIMER7',
        'proc_pin': 'T7', 
        'reg_offset': 0x894, 
        'driver_pin': 37, 
        'proc_pin_name': 'GPMC_OEn_REn', 
        'proc_signal_name': ['gpmc_oen_ren', None, 'timer7', None, None, None, None, 'gpio2_3'], 
        'reset_mode': 7, 
        'gpio_chip': 2,
        'gpio_number': 67,
        'notes': None
    },
    {
        'head_pin':9,
        'head_name': 'TIMER5', 
        'proc_pin': 'T6', 
        'reg_offset': 0x89c, 
        'driver_pin': 39, 
        'proc_pin_name': 'GPMC_BEn0_CLE', 
        'proc_signal_name': ['gpmc_be0n_cle', None, 'timer5', None, None, None, None, 'gpio2_5'], 
        'reset_mode': 7, 
        'gpio_chip': 2,
        'gpio_number': 69,
        'notes': None
    },
    {
    
        'head_pin':10,
        'head_name': 'TIMER6', 
        'proc_pin': 'U6', 
        'reg_offset': 0x898, 
        'driver_pin': 38, 
        'proc_pin_name': 'GPMC_WEn', 
        'proc_signal_name': ['gpmc_wen', None, 'timer6', None, None, None, None, 'gpio2_4'], 
        'reset_mode': 7, 
        'gpio_chip': 2,
        'gpio_number': 68,
        'notes': None
    },
    {
    
        'head_pin':11,
        'head_name': 'GPIO1_13', 
        'proc_pin': 'R12', 
        'reg_offset': 0x834, 
        'driver_pin': 13, 
        'proc_pin_name': 'GPMC_AD13', 
        'proc_signal_name': ['gpmc_ad13', 'lcd_data18', 'mmc1_dat5', 'mmc2_dat1', 'eQEP2B_in', 'pr1_mii0_txd1', 'pr1_pru0_pru_r30_15', 'gpio1_13'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 45,
        'notes': None
    },
    {
    
        'head_pin':12,
        'head_name': 'GPIO1_12', 
        'proc_pin': 'T12', 
        'reg_offset': 0x830, 
        'driver_pin': 12, 
        'proc_pin_name': 'GPMC_AD12', 
        'proc_signal_name': ['gpmc_ad12', 'lcd_data19', 'mmc1_dat4', 'mmc2_dat0', 'eQEP2A_in', 'pr1_mii0_txd2', 'pr1_pru0_pru_r30_14', 'gpio1_12'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 44,
        'notes': None
    },
    {
    
        'head_pin':13,
        'head_name': 'EHRPWM2B', 
        'proc_pin': 'T10', 
        'reg_offset': 0x824,
        'driver_pin': 9, 
        'proc_pin_name': 'GPMC_AD9', 
        'proc_signal_name': ['gpmc_ad9', 'lcd_data22', 'mmc1_dat1', 'mmc2_dat5', 'ehrpwm2B', 'pr1_mii0_col', None, 'gpio0_23'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 23,
        'notes': None
    },
    {
    
        'head_pin':14,
        'head_name': 'GPIO0_26', 
        'proc_pin': 'T11', 
        'reg_offset': 0x828,
        'driver_pin': 10, 
        'proc_pin_name': 'GPMC_AD10', 
        'proc_signal_name': ['gpmc_ad10', 'lcd_data21', 'mmc1_dat2', 'mmc2_dat6', 'ehrpwm2_tripzone_input', 'pr1_mii0_txen', None, 'gpio0_26'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 26,
        'notes': None
    },
    {
    
        'head_pin':15,
        'head_name': 'GPIO1_15', 
        'proc_pin': 'U13', 
        'reg_offset': 0x83c, 
        'driver_pin': 15, 
        'proc_pin_name': 'GPMC_AD15', 
        'proc_signal_name': ['gpmc_ad15', 'lcd_data16', 'mmc1_dat7', 'mmc2_dat3', 'eQEP2_strobe', 'pr1_ecap0_ecap_capin_apwm_o', 'pr1_pru0_pru_r31_15', 'gpio1_15'], 
        'reset_mode': 7, 
        'gpio_chip': 32,
        'gpio_number': 47,
        'notes': None
    },
    {
    
        'head_pin':16,
        'head_name': 'GPIO1_14', 
        'proc_pin': 'V13', 
        'reg_offset': 0x838, 
        'driver_pin': 14, 
        'proc_pin_name': 'GPMC_AD14', 
        'proc_signal_name': ['gpmc_ad14', 'lcd_data17', 'mmc1_dat6', 'mmc2_dat2', 'eQEP2_index', 'pr1_mii0_txd0', 'pr1_pru0_pru_r31_14', 'gpio1_14'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 46,
        'notes': None
    },
    {
    
        'head_pin':17,
        'head_name': 'GPIO0_27', 
        'proc_pin': 'U12', 
        'reg_offset': 0x82c, 
        'driver_pin': 11, 
        'proc_pin_name': 'GPMC_AD11', 
        'proc_signal_name': ['gpmc_ad11', 'lcd_data20', 'mmc1_dat3', 'mmc2_dat7', 'ehrpwm0_synco', 'pr1_mii0_txd3', None, 'gpio0_27'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 27,
        'notes': None
    },
    {
    
        'head_pin':18,
        'head_name': 'GPIO2_1', 
        'proc_pin': 'V12', 
        'reg_offset': 0x88c, 
        'driver_pin': 35, 
        'proc_pin_name': 'GPMC_CLK', 
        'proc_signal_name': ['gpmc_clk', 'lcd_memory_clk', 'gpmc_wait1', 'mmc2_clk', 'pr1_mii1_crs', 'pr1_mdio_mdclk', 'mcasp0_fsr', 'gpio2_1'], 
        'reset_mode': 7, 
        'gpio_chip': 2,
        'gpio_number': 65,
        'notes': None
    },
    {
    
        'head_pin':19,
        'head_name': 'EHRPWM2A', 
        'proc_pin': 'U10', 
        'reg_offset': 0x820, 
        'driver_pin': 8, 
        'proc_pin_name': 'GPMC_AD8', 
        'proc_signal_name': ['gpmc_ad8', 'lcd_data23', 'mmc1_dat0', 'mmc2_dat4', 'ehrpwm2A', 'pr1_mii_mt0_clk', None, 'gpio0_22'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 22,
        'notes': None
    },
    {
    
        'head_pin':20,
        'head_name': 'GPIO1_31', 
        'proc_pin': 'V9', 
        'reg_offset': 0x884, 
        'driver_pin': 33, 
        'proc_pin_name': 'GPMC_CSn2', 
        'proc_signal_name': ['gpmc_csn2', 'gpmc_be1n', 'mmc1_cmd', 'pr1_edio_data_in7', 'pr1_edio_data_out7', 'pr1_pru1_pru_r30_13', 'pr1_pru1_pru_r31_13', 'gpio1_31'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 63,
        'notes': None
    },
    {
    
        'head_pin':21,
        'head_name': 'GPIO1_30',
        'proc_pin': 'U9',
        'reg_offset': 0x880,
        'driver_pin': 32,
        'proc_pin_name': 'GPMC_CSn1',
        'proc_signal_name': ['gpmc_csn1', 'gpmc_clk', 'mmc1_clk', 'pr1_edio_data_in6', 'pr1_edio_data_out6', 'pr1_pru1_pru_r30_12', 'pr1_pru1_pru_r31_12', 'gpio1_30'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 62,
        'notes': None
    },
    {
    
        'head_pin':22,
        'head_name': 'GPIO1_5',
        'proc_pin': 'V8',
        'reg_offset': 0x814,
        'driver_pin': 5,
        'proc_pin_name': 'GPMC_AD5',
        'proc_signal_name': ['gpmc_ad5', 'mmc1_dat5', None, None, None, None, None, 'gpio1_5'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 37,
        'notes': None
    },
    {
    
        'head_pin':23,
        'head_name': 'GPIO1_4',
        'proc_pin': 'U8',
        'reg_offset': 0x810,
        'driver_pin': 4,
        'proc_pin_name': 'GPMC_AD5',
        'proc_signal_name': ['gpmc_ad5', 'mmc1_dat5', None, None, None, None, None, 'gpio1_5'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 37,
        'notes': None
    },
    {
    
        'head_pin':24,
        'head_name': 'GPIO1_1',
        'proc_pin': 'V7',
        'reg_offset': 0x804,
        'driver_pin': 1,
        'proc_pin_name': 'GPMC_AD1',
        'proc_signal_name': ['gpmc_ad1', 'mmc1_dat1', None, None, None, None, None, 'gpio1_1'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 33,
        'notes': None
    },
    {
    
        'head_pin':25,
        'head_name': 'GPIO1_0',
        'proc_pin': 'U7',
        'reg_offset': 0x800,
        'driver_pin': 0,
        'proc_pin_name': 'GPMC_AD0',
        'proc_signal_name': ['gpmc_ad0', 'mmc1_dat0', None, None, None, None, None, 'gpio1_0'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 32,
        'notes': None
    },
    {
    
        'head_pin':26,
        'head_name': 'GPIO1_29',
        'proc_pin': 'V6',
        'reg_offset': 0x87c,
        'driver_pin': 31,
        'proc_pin_name': 'GPMC_CSn0',
        'proc_signal_name': ['gpmc_csn0', None, None, None, None, None, None, 'gpio1_29'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 61,
        'notes': None
    },
    {
    
        'head_pin':27,
        'head_name': 'GPIO2_22',
        'proc_pin': 'U5',
        'reg_offset': 0x8e0,
        'driver_pin': 56,
        'proc_pin_name': 'LCD_VSYNC',
        'proc_signal_name': ['lcd_vsync', 'gpmc_a8', 'gpmc_a1', 'pr1_edio_data_in2', 'pr1_edio_data_out2', 'pr1_pru1_pru_r30_8', 'pr1_pru1_pru_r31_8', 'gpio2_22'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 86,
        'notes': None
    },
    {
    
        'head_pin':28,
        'head_name': 'GPIO2_24',
        'proc_pin': 'V5',
        'reg_offset': 0x8e8,
        'driver_pin': 58,
        'proc_pin_name': 'LCD_PCLK',
        'proc_signal_name': ['lcd_pclk', 'gpmc_a10', 'pr1_mii0_crs', 'pr1_edio_data_in4', 'pr1_edio_data_out4', 'pr1_pru1_pru_r30_10', 'pr1_pru1_pru_r31_10', 'gpio2_24'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 88,
        'notes': None
    },
    {
    
        'head_pin':29,
        'head_name': 'GPIO2_23',
        'proc_pin': 'R5',
        'reg_offset': 0x8e4,
        'driver_pin': 57,
        'proc_pin_name': 'LCD_HSYNC',
        'proc_signal_name': ['lcd_hsync', 'gpmc_a9', 'gpmc_a2', 'pr1_edio_data_in3', 'pr1_edio_data_out3', 'pr1_pru1_pru_r30_9', 'pr1_pru1_pru_r31_9', 'gpio2_23'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 87,
        'notes': None
    },
    {
    
        'head_pin':30,
        'head_name': 'GPIO2_25',
        'proc_pin': 'R6',
        'reg_offset': 0x8ec,
        'driver_pin': 59,
        'proc_pin_name': 'LCD_AC_BIAS_EN',
        'proc_signal_name': ['lcd_ac_bias_en', 'gpmc_a11', 'pr1_mii1_crs', 'pr1_edio_data_in5', 'pr1_edio_data_out5', 'pr1_pru1_pru_r30_11', 'pr1_pru1_pru_r31_11', 'gpio2_25'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 89,
        'notes': None
    },
    {
    
        'head_pin':31,
        'head_name': 'UART5_CTSN',
        'proc_pin': 'V4',
        'reg_offset': 0x8d8,
        'driver_pin': 54,
        'proc_pin_name': 'LCD_DATA14',
        'proc_signal_name': ['lcd_data14', 'gpmc_a18', 'eQEP1_index', 'mcasp0_axr1', 'uart5_rxd', 'pr1_mii_mr0_clk', 'uart5_ctsn', 'gpio0_10'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 10,
        'notes': None
    },
    {
    
        'head_pin':32,
        'head_name': 'UART5_RTSN',
        'proc_pin': 'T5',
        'reg_offset': 0x8dc,
        'driver_pin': 55,
        'proc_pin_name': 'LCD_DATA15',
        'proc_signal_name': ['lcd_data15', 'gpmc_a19', 'eQEP1_strobe', 'mcasp0_ahclkx', 'mcasp0_axr3', 'pr1_mii0_rxdv', 'uart5_rtsn', 'gpio0_11'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 11,
        'notes': None
    },
    {
    
        'head_pin':33,
        'head_name': 'UART4_RTSN',
        'proc_pin': 'V3',
        'reg_offset': 0x8d4,
        'driver_pin': 53,
        'proc_pin_name': 'LCD_DATA13',
        'proc_signal_name': ['lcd_data13', 'gpmc_a17', 'eQEP1B_in', 'mcasp0_fsr', 'mcasp0_axr3', 'pr1_mii0_rxer', 'uart4_rtsn', 'gpio0_9'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 9,
        'notes': None
    },
    {
    
        'head_pin':34,
        'head_name': 'UART3_RTSN',
        'proc_pin': 'U4',
        'reg_offset': 0x8cc,
        'driver_pin': 51,
        'proc_pin_name': 'LCD_DATA11',
        'proc_signal_name': ['lcd_data11', 'gpmc_a15', 'ehrpwm1B', 'mcasp0_ahclkr', 'mcasp0_axr2', 'pr1_mii0_rxd0', 'uart3_rtsn', 'gpio2_17'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 81,
        'notes': None
    },
    {
    
        'head_pin':35,
        'head_name': 'UART4_CTSN',
        'proc_pin': 'V2',
        'reg_offset': 0x8d0,
        'driver_pin': 52,
        'proc_pin_name': 'LCD_DATA12',
        'proc_signal_name': ['lcd_data12', 'gpmc_a16', 'eQEP1A_in', 'mcasp0_aclkr', 'mcasp0_axr2', 'pr1_mii0_rxlink', 'uart4_ctsn', 'gpio0_8'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 8,
        'notes': None
    },
    {
    
        'head_pin':36,
        'head_name': 'UART3_CTSN',
        'proc_pin': 'U3',
        'reg_offset': 0x8c8,
        'driver_pin': 50,
        'proc_pin_name': 'LCD_DATA10',
        'proc_signal_name': ['lcd_data10', 'gpmc_a14', 'ehrpwm1A', 'mcasp0_axr0', None, 'pr1_mii0_rxd1', 'uart3_ctsn', 'gpio2_16'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 80,
        'notes': None
    },
    {
    
        'head_pin':37,
        'head_name': 'UART5_TXD',
        'proc_pin': 'U1',
        'reg_offset': 0x8c0,
        'driver_pin': 48,
        'proc_pin_name': 'LCD_DATA8',
        'proc_signal_name': ['lcd_data8', 'gpmc_a12', 'ehrpwm1_tripzone_input', 'mcasp0_aclkx', 'uart5_txd', 'pr1_mii0_rxd3', 'uart2_ctsn', 'gpio2_14'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 78,
        'notes': None
    },
    {
    
        'head_pin':38,
        'head_name': 'UART5_RXD',
        'proc_pin': 'U2',
        'reg_offset': 0x8c4,
        'driver_pin': 49,
        'proc_pin_name': 'LCD_DATA9',
        'proc_signal_name': ['lcd_data9', 'gpmc_a13', 'ehrpwm0_synco', 'mcasp0_fsx', 'uart5_rxd', 'pr1_mii0_rxd2', 'uart2_rtsn', 'gpio2_15'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 79,
        'notes': None
    },
    {
    
        'head_pin':39,
        'head_name': 'GPIO2_12',
        'proc_pin': 'T3',
        'reg_offset': 0x8b8,
        'driver_pin': 46,
        'proc_pin_name': 'LCD_DATA6',
        'proc_signal_name': ['lcd_data6', 'gpmc_a6', 'pr1_edio_data_in6', 'eQEP2_index', 'pr1_edio_data_out6', 'pr1_pru1_pru_r30_6', 'pr1_pru1_pru_r31_6', 'gpio2_12'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 76,
        'notes': None
    },
    {
    
        'head_pin':40,
        'head_name': 'GPIO2_13',
        'proc_pin': 'T4',
        'reg_offset': 0x8bc,
        'driver_pin': 47,
        'proc_pin_name': 'LCD_DATA7',
        'proc_signal_name': ['lcd_data7', 'gpmc_a7', 'pr1_edio_data_in7', 'eQEP2_strobe', 'pr1_edio_data_out7', 'pr1_pru1_pru_r30_7', 'pr1_pru1_pru_r31_7', 'gpio2_13'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 77,
        'notes': None
    },
    {
    
        'head_pin':41,
        'head_name': 'GPIO2_10',
        'proc_pin': 'T1',
        'reg_offset': 0x8b0,
        'driver_pin': 44,
        'proc_pin_name': 'LCD_DATA4',
        'proc_signal_name': ['lcd_data4', 'gpmc_a4', 'pr1_mii0_txd1', 'eQEP2A_in', None, 'pr1_pru1_pru_r30_4', 'pr1_pru1_pru_r31_4', 'gpio2_10'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 74,
        'notes': None
    },
    {
    
        'head_pin':42,
        'head_name': 'GPIO2_11',
        'proc_pin': 'T2',
        'reg_offset': 0x8b4,
        'driver_pin': 45,
        'proc_pin_name': 'LCD_DATA5',
        'proc_signal_name': ['lcd_data5', 'gpmc_a5', 'pr1_mii0_txd0', 'eQEP2B_in', None, 'pr1_pru1_pru_r30_5', 'pr1_pru1_pru_r31_5', 'gpio2_11'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 75,
        'notes': None
    },
    {
    
        'head_pin':43,
        'head_name': 'GPIO2_8',
        'proc_pin': 'R3',
        'reg_offset': 0x8a8,
        'driver_pin': 42,
        'proc_pin_name': 'LCD_DATA2',
        'proc_signal_name': ['lcd_data2', 'gpmc_a2', 'pr1_mii0_txd3', 'ehrpwm2_tripzone_input', None, 'pr1_pru1_pru_r30_2', 'pr1_pru1_pru_r31_2', 'gpio2_8'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 72,
        'notes': None
    },
    {
    
        'head_pin':44,
        'head_name': 'GPIO2_9',
        'proc_pin': 'R4',
        'reg_offset': 0x8ac,
        'driver_pin': 43,
        'proc_pin_name': 'LCD_DATA3',
        'proc_signal_name': ['lcd_data3', 'gpmc_a3', 'pr1_mii0_txd2', 'ehrpwm0_synco', None, 'pr1_pru1_pru_r30_3', 'pr1_pru1_pru_r31_3', 'gpio2_9'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 73,
        'notes': None
    },
    {
    
        'head_pin':45,
        'head_name': 'GPIO2_6',
        'proc_pin': 'R1',
        'reg_offset': 0x8a0,
        'driver_pin': 40,
        'proc_pin_name': 'LCD_DATA0',
        'proc_signal_name': ['lcd_data0', 'gpmc_a0', 'pr1_mii_mt0_clk', 'ehrpwm2A', None, 'pr1_pru1_pru_r30_0', 'pr1_pru1_pru_r31_0', 'gpio2_6'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 70,
        'notes': None
    },
    {
    
        'head_pin':46,
        'head_name': 'GPIO2_7',
        'proc_pin': 'R2',
        'reg_offset': 0x8a4,
        'driver_pin': 41,
        'proc_pin_name': 'LCD_DATA1',
        'proc_signal_name': ['lcd_data1', 'gpmc_a1', 'pr1_mii0_txen', 'ehrpwm2B', None, 'pr1_pru1_pru_r30_1', 'pr1_pru1_pru_r31_1', 'gpio2_7'],
        'reset_mode': 7,
        'gpio_chip': 2,
        'gpio_number': 71,
        'notes': None
    }
]

############################################################################
# P9 header definition
# 
# See P8 comment over for array description
#
############################################################################
BBB_P9_DEF = [
    {
    
        'head_pin':1,
        'head_name': 'GND', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'GND'
    },
    {
    
        'head_pin':2,
        'head_name': 'GND', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None, 
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'GND'
    },
    {
    
        'head_pin':3,
        'head_name': 'DC_3.3V', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'DC_3.3V'
    },
    {
    
        'head_pin':4,
        'head_name': 'DC_3.3V', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'DC_3.3V'
    },
    {
    
        'head_pin':5,
        'head_name': 'VDD_5V', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'VDD_5V'
    },
    {
    
        'head_pin':6,
        'head_name': 'VDD_5V', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'VDD_5V'
    },
    {
    
        'head_pin':7,
        'head_name': 'SYS_5V', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'SYS_5V'
    },
    {
    
        'head_pin':8,
        'head_name': 'SYS_5V', 
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'SYS_5V'
    },
    {
    
        'head_pin':9,
        'head_name': 'PWR_BUT',
        'proc_pin': None, 
        'reg_offset': None, 
        'driver_pin': None, 
        'proc_pin_name': None, 
        'proc_signal_name': [None, None, None, None, None, None, None, None], 
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': 'PWR_BUT'
    },
    {
    
        'head_pin':10,
        'head_name': 'SYS_RESETn', 
        'proc_pin': 'A10', 
        'reg_offset': 0x9b8, 
        'driver_pin': 110, 
        'proc_pin_name': 'WARMRSTn', 
        'proc_signal_name': ['nRESETIN_OUT', None, None, None, None, None, None, None], 
        'reset_mode': 0, 
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':11,
        'head_name': 'UART4_RXD', 
        'proc_pin': 'T17', 
        'reg_offset': 0x870, 
        'driver_pin': 28, 
        'proc_pin_name': 'GPMC_WAIT0', 
        'proc_signal_name': ['gpmc_wait0', 'gmii2_crs', 'gpmc_csn4', 'rmii2_crs_dv', 'mmc1_sdcd', 'pr1_mii1_col', 'uart4_rxd', 'gpio0_30'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 30,
        'notes': None
    },
    {
    
        'head_pin':12,
        'head_name': 'GPIO1_28',
        'proc_pin': 'U18', 
        'reg_offset': 0x878, 
        'driver_pin': 30, 
        'proc_pin_name': 'GPMC_BEn1', 
        'proc_signal_name': ['gpmc_be1n', 'gmii2_col', 'gpmc_csn6', 'mmc2_dat3', 'gpmc_dir', 'pr1_mii1_rxlink', 'mcasp0_aclkr', 'gpio1_28'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 60,
        'notes': None
    },
    {
    
        'head_pin':13,
        'head_name': 'UART4_TXD', 
        'proc_pin': 'U17', 
        'reg_offset': 0x874,
        'driver_pin': 29, 
        'proc_pin_name': 'GPMC_WPn', 
        'proc_signal_name': ['gpmc_wpn', 'gmii2_rxerr', 'gpmc_csn5', 'rmii2_rxerr', 'mmc2_sdcd', 'pr1_mii1_txen', 'uart4_txd', 'gpio0_31'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 31,
        'notes': None
    },
    {
    
        'head_pin':14,
        'head_name': 'EHRPWM1A', 
        'proc_pin': 'U14', 
        'reg_offset': 0x848,
        'driver_pin': 18, 
        'proc_pin_name': 'GPMC_A2', 
        'proc_signal_name': ['gpmc_a2', 'gmii2_txd3', 'rgmii2_td3', 'mmc2_dat1', 'gpmc_a18', 'pr1_mii1_txd2', 'ehrpwm1A', 'gpio1_18'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 50,
        'notes': None
    },
    {
    
        'head_pin':15,
        'head_name': 'GPIO1_16', 
        'proc_pin': 'R13', 
        'reg_offset': 0x840, 
        'driver_pin': 16, 
        'proc_pin_name': 'GPMC_A0', 
        'proc_signal_name': ['gpmc_a0', 'gmii2_txen', 'rgmii2_tctl', 'rmii2_txen', 'gpmc_a16', 'pr1_mii_mt1_clk', 'ehrpwm1_tripzone_input', 'gpio1_16'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 48,
        'notes': None
    },
    {
    
        'head_pin':16,
        'head_name': 'EHRPWM1B', 
        'proc_pin': 'T14', 
        'reg_offset': 0x84c, 
        'driver_pin': 19, 
        'proc_pin_name': 'GPMC_A3', 
        'proc_signal_name': ['gpmc_a3', 'gmii2_txd2', 'rgmii2_td2', 'mmc2_dat2', 'gpmc_a19', 'pr1_mii1_txd1', 'ehrpwm1B', 'gpio1_19'], 
        'reset_mode': 7, 
        'gpio_chip': 1,
        'gpio_number': 51,
        'notes': None
    },
    {
    
        'head_pin':17,
        'head_name': 'I2C1_SCL', 
        'proc_pin': 'A16', 
        'reg_offset': 0x95c, 
        'driver_pin': 87, 
        'proc_pin_name': 'SPI0_CS0', 
        'proc_signal_name': ['spi0_cs0', 'mmc2_sdwp', 'I2C1_SCL', 'ehrpwm0_synci', 'pr1_uart0_txd', 'pr1_edio_data_in1', 'pr1_edio_data_out1', 'gpio0_5'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 5,
        'notes': None
    },
    {
    
        'head_pin':18,
        'head_name': 'I2C1_SDA', 
        'proc_pin': 'B16', 
        'reg_offset': 0x958, 
        'driver_pin': 86, 
        'proc_pin_name': 'SPI0_D1', 
        'proc_signal_name': ['spi0_d1', 'mmc1_sdwp', 'I2C1_SDA', 'ehrpwm0_tripzone_input', 'pr1_uart0_rxd', 'pr1_edio_data_in0', 'pr1_edio_data_out0', 'gpio0_4'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 4,
        'notes': None
    },
    {
    
        'head_pin':19,
        'head_name': 'I2C2_SCL', 
        'proc_pin': 'D17', 
        'reg_offset': 0x97c, 
        'driver_pin': 95, 
        'proc_pin_name': 'UART1_RTSn', 
        'proc_signal_name': ['uart1_rtsn', 'timer5', 'dcan0_rx', 'I2C2_SCL', 'spi1_cs1', 'pr1_uart0_rts_n', 'pr1_edc_latch1_in', 'gpio0_13'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 13,
        'notes': None
    },
    {
    
        'head_pin':20,
        'head_name': 'I2C2_SDA', 
        'proc_pin': 'D18', 
        'reg_offset': 0x978, 
        'driver_pin': 94, 
        'proc_pin_name': 'UART1_CTSn', 
        'proc_signal_name': ['uart1_ctsn', 'timer6', 'dcan0_tx', 'I2C2_SDA', 'spi1_cs0', 'pr1_uart0_cts_n', 'pr1_edc_latch0_in', 'gpio0_12'], 
        'reset_mode': 7, 
        'gpio_chip': 0,
        'gpio_number': 12,
        'notes': None
    },
    {
    
        'head_pin':21,
        'head_name': 'UART2_TXD',
        'proc_pin': 'B17',
        'reg_offset': 0x954,
        'driver_pin': 85,
        'proc_pin_name': 'SPI0_D0',
        'proc_signal_name': ['spi0_d0', 'uart2_txd', 'I2C2_SCL', 'ehrpwm0B', 'pr1_uart0_rts_n', 'pr1_edio_latch_in', 'EMU3', 'gpio0_3'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 3,
        'notes': None
    },
    {
    
        'head_pin':22,
        'head_name': 'UART2_RXD',
        'proc_pin': 'A17',
        'reg_offset': 0x950,
        'driver_pin': 84,
        'proc_pin_name': 'SPI0_SCLK',
        'proc_signal_name': ['spi0_sclk', 'uart2_rxd', 'I2C2_SDA', 'ehrpwm0A', 'pr1_uart0_cts_n', 'pr1_edio_sof', 'EMU2', 'gpio0_2'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 2,
        'notes': None
    },
    {
    
        'head_pin':23,
        'head_name': 'GPIO1_17',
        'proc_pin': 'V14',
        'reg_offset': 0x844,
        'driver_pin': 17,
        'proc_pin_name': 'GPMC_A1',
        'proc_signal_name': ['gpmc_a1', 'gmii2_rxdv', 'rgmii2_rctl', 'mmc2_dat0', 'gpmc_a17', 'pr1_mii1_txd3', 'ehrpwm0_synco', 'gpio1_17'],
        'reset_mode': 7,
        'gpio_chip': 1,
        'gpio_number': 49,
        'notes': None
    },
    {
    
        'head_pin':24,
        'head_name': 'UART1_TXD',
        'proc_pin': 'D15',
        'reg_offset': 0x984,
        'driver_pin': 97,
        'proc_pin_name': 'GPMC_AD1',
        'proc_signal_name': ['uart1_txd', 'mmc2_sdwp', 'dcan1_rx', 'I2C1_SCL', None, 'pr1_uart0_txd', 'pr1_pru0_pru_r31_16', 'gpio0_15'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 15,
        'notes': None
    },
    {
    
        'head_pin':25,
        'head_name': 'GPIO3_21',
        'proc_pin': 'A14',
        'reg_offset': 0x9ac,
        'driver_pin': 107,
        'proc_pin_name': 'MCASP0_AHCLKX',
        'proc_signal_name': ['mcasp0_ahclkx', 'eQEP0_strobe', 'mcasp0_axr3', 'mcasp1_axr1', 'EMU4', 'pr1_pru0_pru_r30_7', 'pr1_pru0_pru_r31_7', 'gpio3_21'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 117,
        'notes': None
    },
    {
    
        'head_pin':26,
        'head_name': 'UART1_RXD',
        'proc_pin': 'D16',
        'reg_offset': 0x980,
        'driver_pin': 96,
        'proc_pin_name': 'UART1_RXD',
        'proc_signal_name': ['uart1_rxd', 'mmc1_sdwp', 'dcan1_tx', 'I2C1_SDA', None, 'pr1_uart0_rxd', 'pr1_pru1_pru_r31_16', 'gpio0_14'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 14,
        'notes': None
    },
    {
    
        'head_pin':27,
        'head_name': 'GPIO3_19',
        'proc_pin': 'C13',
        'reg_offset': 0x9a4,
        'driver_pin': 105,
        'proc_pin_name': 'MCASP0_FSR',
        'proc_signal_name': ['mcasp0_fsr', 'eQEP0B_in', 'mcasp0_axr3', 'mcasp1_fsx', 'EMU2', 'pr1_pru0_pru_r30_5', 'pr1_pru0_pru_r31_5', 'gpio3_19'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 115,
        'notes': None
    },
    {
    
        'head_pin':28,
        'head_name': 'SPI1_CS0',
        'proc_pin': 'C12',
        'reg_offset': 0x99c,
        'driver_pin': 103,
        'proc_pin_name': 'MCASP0_AHCLKR',
        'proc_signal_name': ['mcasp0_ahclkr', 'ehrpwm0_synci', 'mcasp0_axr2', 'spi1_cs0', 'eCAP2_in_PWM2_out', 'pr1_pru0_pru_r30_3', 'pr1_pru0_pru_r31_3', 'gpio3_17'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 113,
        'notes': None
    },
    {
    
        'head_pin':29,
        'head_name': 'SPI1_D0',
        'proc_pin': 'B13',
        'reg_offset': 0x994,
        'driver_pin': 101,
        'proc_pin_name': 'MCASP0_FSX',
        'proc_signal_name': ['mcasp0_fsx', 'ehrpwm0B', None, 'spi1_d0', 'mmc1_sdcd', 'pr1_pru0_pru_r30_1', 'pr1_pru0_pru_r31_1', 'gpio3_15'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 111,
        'notes': None
    },
    {
    
        'head_pin':30,
        'head_name': 'SPI1_D1',
        'proc_pin': 'D12',
        'reg_offset': 0x998,
        'driver_pin': 102,
        'proc_pin_name': 'MCASP0_AXR0',
        'proc_signal_name': ['mcasp0_axr0', 'ehrpwm0_tripzone_input', None, 'spi1_d1', 'mmc2_sdcd', 'pr1_pru0_pru_r30_2', 'pr1_pru0_pru_r31_2', 'gpio3_16'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 112,
        'notes': None
    },
    {
    
        'head_pin':31,
        'head_name': 'SPI1_SCLK',
        'proc_pin': 'A13',
        'reg_offset': 0x990,
        'driver_pin': 100,
        'proc_pin_name': 'MCASP0_ACLKX',
        'proc_signal_name': ['mcasp0_aclkx', 'ehrpwm0A', None, 'spi1_sclk', 'mmc0_sdcd', 'pr1_pru0_pru_r30_0', 'pr1_pru0_pru_r31_0', 'gpio3_14'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 110,
        'notes': None
    },
    {
    
        'head_pin':32,
        'head_name': 'VADC',
        'proc_pin': None,
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': None,
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':33,
        'head_name': 'AIN4',
        'proc_pin': 'C8',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN4',
        'proc_signal_name': ['AIN4', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':34,
        'head_name': 'AGND',
        'proc_pin': None,
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': None,
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':35,
        'head_name': 'AIN8',
        'proc_pin': 'A8',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN8',
        'proc_signal_name': ['AIN8', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':36,
        'head_name': 'AIN5',
        'proc_pin': 'B8',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN5',
        'proc_signal_name': ['AIN5', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':37,
        'head_name': 'AIN2',
        'proc_pin': 'B7',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN2',
        'proc_signal_name': ['AIN2', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':38,
        'head_name': 'AIN3',
        'proc_pin': 'A7',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN3',
        'proc_signal_name': ['AIN3', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':39,
        'head_name': 'AIN0',
        'proc_pin': 'B6',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN0',
        'proc_signal_name': ['AIN0', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':40,
        'head_name': 'AIN1',
        'proc_pin': 'C7',
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': 'AIN1',
        'proc_signal_name': ['AIN1', None, None, None, None, None, None, None],
        'reset_mode': 0,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':411,    #This is not a mistake
        'head_name': 'CLKOUT2',
        'proc_pin': 'D14',
        'reg_offset': 0x9b4,
        'driver_pin': 109,
        'proc_pin_name': 'XDMA_EVENT_INTR1',
        'proc_signal_name': ['xdma_event_intr1', None, 'tclkin', 'clkout2', 'timer7', 'pr1_pru0_pru_r31_16', 'EMU3', 'gpio0_20'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 20,
        'notes': None
    },
    {
    
        'head_pin':412,
        'head_name': 'GPIO3_20',
        'proc_pin': 'D13',
        'reg_offset': 0x9a8,
        'driver_pin': 106,
        'proc_pin_name': 'MCASP0_AXR1',
        'proc_signal_name': ['mcasp0_axr1', 'eQEP0_index', None, 'mcasp1_axr0', 'EMU3', 'pr1_pru0_pru_r30_6', 'pr1_pru0_pru_r31_6', 'gpio3_20'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 114,
        'notes': None
    },
    {
    
        'head_pin':421,
        'head_name': 'GPIO0_7',
        'proc_pin': 'C18',
        'reg_offset': 0x964,
        'driver_pin': 89,
        'proc_pin_name': 'ECAP0_IN_PWM0_OUT',
        'proc_signal_name': ['eCAP0_in_PWM0_out', 'uart3_txd', 'spi1_cs1', 'pr1_ecap0_ecap_capin_apwm_o', 'spi1_sclk', 'mmc0_sdwp', 'xdma_event_intr2', 'gpio0_7'],
        'reset_mode': 7,
        'gpio_chip': 0,
        'gpio_number': 7,
        'notes': None
    },
    {
    
        'head_pin':422,
        'head_name': 'GPIO3_18',
        'proc_pin': 'B12',
        'reg_offset': 0x9a0,
        'driver_pin': 104,
        'proc_pin_name': 'MCASP0_ACLKR',
        'proc_signal_name': ['mcasp0_aclkr', 'eQEP0A_in', 'mcasp0_axr2', 'mcasp1_aclkx', 'mmc0_sdwp', 'pr1_pru0_pru_r30_4', 'pr1_pru0_pru_r31_4', 'gpio3_18'],
        'reset_mode': 7,
        'gpio_chip': 3,
        'gpio_number': 114,
        'notes': None
    },
    {
    
        'head_pin':43,
        'head_name': 'GND',
        'proc_pin': None,
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': None,
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':44,
        'head_name': 'GND',
        'proc_pin': None,
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': None,
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':45,
        'head_name': 'GND',
        'proc_pin': None,
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': None,
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    },
    {
    
        'head_pin':46,
        'head_name': 'GND',
        'proc_pin': None,
        'reg_offset': None,
        'driver_pin': None,
        'proc_pin_name': None,
        'proc_signal_name': [None, None, None, None, None, None, None, None],
        'reset_mode': None,
        'gpio_chip': None,
        'gpio_number': None,
        'notes': None
    }
]