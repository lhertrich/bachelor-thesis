import chromadb
import openai
import os
from chromadb.utils import embedding_functions

openai.api_key = os.environ.get('OPENAI_API_KEY')

openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")

client = chromadb.PersistentClient(path="/Users/levin/Documents/Uni/6. Semester/Bachelorarbeit/Prototyping/prototype 2.0")

test_collection = client.create_collection(name="test_collection", embedding_function=openai_ef, metadata={"hnsw:space": "cosine"})

test_collection.add(documents=["/**/ /* View: V_Plant_V1_IDIM1 */ /**/ /* =*/ /* V01.00.00 2022-05-04 FRI3SH */ /* This view provides the Plant Code for the application CIVS (Central Inventory */ /* Valuation Solution) of GS. This Dimension is referenced via linked Server by Core Light */ /* Data.CORE Outgoing Interface #0227 https://inside-docupedia.bosch.com/confluence/x/HsYxhg */ /* Restriction: */ /* none */ /* Changes: */ /* V01.00.00 - Initial version */ /* =*/",
                               "/**/ /* View: V_INTF_CDP_CostActual_V2_IFCT0_D4 */ /**/ /* = */ /* V01.00.00 2023-03-15 Ismail Okadia GS/TET3-NA */ /* This view is to provide CO-OM Cost Actuals data for Cost Driver Planning application (CDP) */ /* Data.CORE Outgoing Interface #0337 https://inside-docupedia.bosch.com/confluence/x/RBnSqQ */ /* Implemented Soft Rules */ /* Filter Cost Actual Fact Data by Company Code Positive List */ /* #FBI-SR-000000057 https://inside-docupedia.bosch.com/confluence/x/fFf1Yw */ /* Update: */ /* V01.00.00 Recreated view on top of persisted Fact [COCostActual_V2_MFCT0_D4] */ /* */",
                               "/**/ /* View: V_FactActualCostMaintenanceOrder_G4 */ /**/ /**/ /* V01.00.03 2021-11-23 Szivos Andras CI/BTM-AC1 */ /* Fact view for Costs Maintenance Order booked on Maintenance Orders from P81 */ /* Changes: */ /* - V01.00.03 2021-11-23 Szivos Andras CI/BTM-AC1 Clean up of SQL code */ /* - V01.00.00 2021-09-24 Szivos Andras CI/BTM-AC1 Original version created */ /**/"], 
                    metadatas=[{"ObjectName": "V_Plant_V1_IDIM1", "ObjectName": "V_INTF_CDP_CostActual_V2_IFCT0_D4", "ObjectName": "V_FactActualCostMaintenanceOrder_G4"}], 
                    ids=["105", "69", "51"])

