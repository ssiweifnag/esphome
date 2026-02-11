import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_AIR_QUALITY,
    DEVICE_CLASS_CARBON_DIOXIDE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_HUMIDITY,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_HECTOPASCAL,
    UNIT_PERCENT,
    UNIT_PARTS_PER_BILLION,
    UNIT_PARTS_PER_MILLION,
)

CONF_BME680_ID = "bme680_id"

bme680_ns = cg.esphome_ns.namespace("bme680")
BME680Component = bme680_ns.class_(
    "BME680Component", cg.PollingComponent, i2c.I2CDevice
)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_BME680_ID): cv.use_id(BME680Component),
    cv.Optional("temperature"): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional("pressure"): sensor.sensor_schema(
        unit_of_measurement=UNIT_HECTOPASCAL,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_PRESSURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional("humidity"): sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional("gas_resistance"): sensor.sensor_schema(
        unit_of_measurement="Ω",
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # IAQ (Indoor Air Quality) sensor
    cv.Optional("iaq"): sensor.sensor_schema(
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_AIR_QUALITY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional("iaq_accuracy"): sensor.sensor_schema(
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # VOC (Volatile Organic Compounds) sensor
    cv.Optional("voc"): sensor.sensor_schema(
        unit_of_measurement=UNIT_PARTS_PER_BILLION,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_AIR_QUALITY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # CO2 equivalent sensor
    cv.Optional("co2_equivalent"): sensor.sensor_schema(
        unit_of_measurement=UNIT_PARTS_PER_MILLION,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_CARBON_DIOXIDE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}).extend(cv.polling_component_schema("60s")).extend(i2c.i2c_device_schema(0x77))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_BME680_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if "temperature" in config:
        sens = await sensor.new_sensor(config["temperature"])
        cg.add(var.set_temperature_sensor(sens))

    if "pressure" in config:
        sens = await sensor.new_sensor(config["pressure"])
        cg.add(var.set_pressure_sensor(sens))

    if "humidity" in config:
        sens = await sensor.new_sensor(config["humidity"])
        cg.add(var.set_humidity_sensor(sens))

    if "gas_resistance" in config:
        sens = await sensor.new_sensor(config["gas_resistance"])
        cg.add(var.set_gas_resistance_sensor(sens))

    # IAQ sensors
    if "iaq" in config:
        sens = await sensor.new_sensor(config["iaq"])
        cg.add(var.set_iaq_sensor(sens))
    
    if "iaq_accuracy" in config:
        sens = await sensor.new_sensor(config["iaq_accuracy"])
        cg.add(var.set_iaq_accuracy(sens))
    
    # VOC sensor
    if "voc" in config:
        sens = await sensor.new_sensor(config["voc"])
        cg.add(var.set_voc_sensor(sens))
    
    # CO2 equivalent sensor
    if "co2_equivalent" in config:
        sens = await sensor.new_sensor(config["co2_equivalent"])
        cg.add(var.set_co2_equivalent_sensor(sens))
