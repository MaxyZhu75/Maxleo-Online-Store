#! /bin/bash
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_query_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_query_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_catalog_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_catalog_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_placeOrder_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_placeOrder_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_placeOrder_outofstock
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_buy_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_buy_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_buy_outofstock
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_order_cata_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_order_cata_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_queryOrder_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_app_client_queryOrder_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_queryOrder_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_queryOrder_invalid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_heartbeat_valid
FRONT=3.80.136.186 CATALOG=3.80.136.186 ORDER=3.80.136.186 python -m unittest -v test_func.TestFunctionality.test_microservices_frontend_notifyNewLeader_valid
exec /bin/bash
