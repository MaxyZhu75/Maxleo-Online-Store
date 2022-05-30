#! /bin/bash
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_app_client_query_valid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_app_client_query_invalid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_catalog_valid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_catalog_invalid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_order_valid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_order_invalid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_order_outofstock
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_app_client_buy_valid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_app_client_buy_invalid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_app_client_buy_outofstock
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_order_cata_valid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_order_cata_invalid
FRONT=172.20.0.4 CATALOG=172.20.0.2 ORDER=172.20.0.3 python -m unittest -v test_func.TestFunctionality.test_microservices_order_cata_outofstock
exec /bin/bash
