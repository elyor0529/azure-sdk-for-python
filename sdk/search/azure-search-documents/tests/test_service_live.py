# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import json
from os.path import dirname, join, realpath
import time

import pytest

from devtools_testutils import AzureMgmtTestCase

from search_service_preparer import SearchServicePreparer, SearchResourceGroupPreparer

from azure.core import MatchConditions
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.search.documents.indexes.models import(
    AnalyzeTextOptions,
    AnalyzeResult,
    CorsOptions,
    EntityRecognitionSkill,
    SearchIndex,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    ScoringProfile,
    SearchIndexerSkillset,
    SearchIndexerDataSourceConnection,
    SearchIndexer,
    SearchIndexerDataContainer,
    SynonymMap,
    SimpleField,
    SearchFieldDataType
)
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient

CWD = dirname(realpath(__file__))
SCHEMA = open(join(CWD, "hotel_schema.json")).read()
BATCH = json.load(open(join(CWD, "hotel_small.json")))
TIME_TO_SLEEP = 5
CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=storagename;AccountKey=NzhL3hKZbJBuJ2484dPTR+xF30kYaWSSCbs2BzLgVVI1woqeST/1IgqaLm6QAOTxtGvxctSNbIR/1hW8yH+bJg==;EndpointSuffix=core.windows.net'

class SearchClientTest(AzureMgmtTestCase):

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer()
    def test_get_service_statistics(self, api_key, endpoint, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.get_service_statistics()
        assert isinstance(result, dict)
        assert set(result.keys()) == {"counters", "limits"}

class SearchIndexesClientTest(AzureMgmtTestCase):

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer()
    def test_list_indexes_empty(self, api_key, endpoint, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.list_indexes()
        with pytest.raises(StopIteration):
            next(result)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_list_indexes(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.list_indexes()

        first = next(result)
        assert first.name == index_name

        with pytest.raises(StopIteration):
            next(result)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_index(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.get_index(index_name)
        assert result.name == index_name

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_index_statistics(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.get_index_statistics(index_name)
        assert set(result.keys()) == {'document_count', 'storage_size'}

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_indexes(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        client.delete_index(index_name)
        import time
        if self.is_live:
            time.sleep(TIME_TO_SLEEP)
        result = client.list_indexes()
        with pytest.raises(StopIteration):
            next(result)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_indexes_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))

        # First create an index
        name = "hotels"
        fields = [
        {
          "name": "hotelId",
          "type": "Edm.String",
          "key": True,
          "searchable": False
        },
        {
          "name": "baseRate",
          "type": "Edm.Double"
        }]
        scoring_profile = ScoringProfile(
            name="MyProfile"
        )
        scoring_profiles = []
        scoring_profiles.append(scoring_profile)
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        index = SearchIndex(
            name=name,
            fields=fields,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options)
        result = client.create_index(index)
        etag = result.e_tag
        # get e tag  and update
        index.scoring_profiles = []
        client.create_or_update_index(index)

        index.e_tag = etag
        with pytest.raises(HttpResponseError):
            client.delete_index(index, match_condition=MatchConditions.IfNotModified)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_index(self, api_key, endpoint, index_name, **kwargs):
        name = "hotels"
        fields = [
            SimpleField(name="hotelId", type=SearchFieldDataType.String, key=True),
            SimpleField(name="baseRate", type=SearchFieldDataType.Double)
        ]
        scoring_profile = ScoringProfile(
            name="MyProfile"
        )
        scoring_profiles = []
        scoring_profiles.append(scoring_profile)
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        index = SearchIndex(
            name=name,
            fields=fields,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options)
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.create_index(index)
        assert result.name == "hotels"
        assert result.scoring_profiles[0].name == scoring_profile.name
        assert result.cors_options.allowed_origins == cors_options.allowed_origins
        assert result.cors_options.max_age_in_seconds == cors_options.max_age_in_seconds

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_index(self, api_key, endpoint, index_name, **kwargs):
        name = "hotels"
        fields = [
            SimpleField(name="hotelId", type=SearchFieldDataType.String, key=True),
            SimpleField(name="baseRate", type=SearchFieldDataType.Double)
        ]
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        scoring_profiles = []
        index = SearchIndex(
            name=name,
            fields=fields,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options)
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        result = client.create_or_update_index(index=index)
        assert len(result.scoring_profiles) == 0
        assert result.cors_options.allowed_origins == cors_options.allowed_origins
        assert result.cors_options.max_age_in_seconds == cors_options.max_age_in_seconds
        scoring_profile = ScoringProfile(
            name="MyProfile"
        )
        scoring_profiles = []
        scoring_profiles.append(scoring_profile)
        index = SearchIndex(
            name=name,
            fields=fields,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options)
        result = client.create_or_update_index(index=index)
        assert result.scoring_profiles[0].name == scoring_profile.name
        assert result.cors_options.allowed_origins == cors_options.allowed_origins
        assert result.cors_options.max_age_in_seconds == cors_options.max_age_in_seconds

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_indexes_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))

        # First create an index
        name = "hotels"
        fields = [
        {
          "name": "hotelId",
          "type": "Edm.String",
          "key": True,
          "searchable": False
        },
        {
          "name": "baseRate",
          "type": "Edm.Double"
        }]
        scoring_profile = ScoringProfile(
            name="MyProfile"
        )
        scoring_profiles = []
        scoring_profiles.append(scoring_profile)
        cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
        index = SearchIndex(
            name=name,
            fields=fields,
            scoring_profiles=scoring_profiles,
            cors_options=cors_options)
        result = client.create_index(index)
        etag = result.e_tag
        # get e tag  and update
        index.scoring_profiles = []
        client.create_or_update_index(index)

        index.e_tag = etag
        with pytest.raises(HttpResponseError):
            client.create_or_update_index(index, match_condition=MatchConditions.IfNotModified)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_analyze_text(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        analyze_request = AnalyzeTextOptions(text="One's <two/>", analyzer_name="standard.lucene")
        result = client.analyze_text(index_name, analyze_request)
        assert len(result.tokens) == 2

class SearchSynonymMapsClientTest(AzureMgmtTestCase):
    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_synonym_map(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ])
        synonym_map = SynonymMap(name="test-syn-map", synonyms=solr_format_synonyms)
        result = client.create_synonym_map(synonym_map)
        assert isinstance(result, SynonymMap)
        assert result.name == "test-syn-map"
        assert result.synonyms == [
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ]
        assert len(client.get_synonym_maps()) == 1

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_synonym_map(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ])
        synonym_map = SynonymMap(name="test-syn-map", synonyms=solr_format_synonyms)
        result = client.create_synonym_map(synonym_map)
        assert len(client.get_synonym_maps()) == 1
        client.delete_synonym_map("test-syn-map")
        assert len(client.get_synonym_maps()) == 0

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_synonym_map_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ])
        synonym_map = SynonymMap(name="test-syn-map", synonyms=solr_format_synonyms)
        result = client.create_synonym_map(synonym_map)
        etag = result.e_tag

        synonym_map.synonyms = "\n".join([
            "Washington, Wash. => WA",
        ])
        client.create_or_update_synonym_map(synonym_map)

        result.e_tag = etag
        with pytest.raises(HttpResponseError):
            client.delete_synonym_map(result, match_condition=MatchConditions.IfNotModified)
            assert len(client.get_synonym_maps()) == 1

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_synonym_map(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ])
        synonym_map = SynonymMap(name="test-syn-map", synonyms=solr_format_synonyms)
        client.create_synonym_map(synonym_map)
        assert len(client.get_synonym_maps()) == 1
        result = client.get_synonym_map("test-syn-map")
        assert isinstance(result, SynonymMap)
        assert result.name == "test-syn-map"
        assert result.synonyms == [
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ]

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_synonym_maps(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
        ])
        synonym_map_1 = SynonymMap(name="test-syn-map-1", synonyms=solr_format_synonyms)
        client.create_synonym_map(synonym_map_1)
        solr_format_synonyms = "\n".join([
            "Washington, Wash. => WA",
        ])
        synonym_map_2 = SynonymMap(name="test-syn-map-2", synonyms=solr_format_synonyms)
        client.create_synonym_map(synonym_map_2)
        result = client.get_synonym_maps()
        assert isinstance(result, list)
        assert all(isinstance(x, SynonymMap) for x in result)
        assert set(x.name for x in result) == {"test-syn-map-1", "test-syn-map-2"}

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_synonym_map(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ])
        synonym_map = SynonymMap(name="test-syn-map", synonyms=solr_format_synonyms)
        client.create_synonym_map(synonym_map)
        assert len(client.get_synonym_maps()) == 1
        synonym_map.synonyms = "\n".join([
            "Washington, Wash. => WA",
        ])
        client.create_or_update_synonym_map(synonym_map)
        assert len(client.get_synonym_maps()) == 1
        result = client.get_synonym_map("test-syn-map")
        assert isinstance(result, SynonymMap)
        assert result.name == "test-syn-map"
        assert result.synonyms == [
            "Washington, Wash. => WA",
        ]

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_synonym_map_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexClient(endpoint, AzureKeyCredential(api_key))
        solr_format_synonyms = "\n".join([
            "USA, United States, United States of America",
            "Washington, Wash. => WA",
        ])
        synonym_map = SynonymMap(name="test-syn-map", synonyms=solr_format_synonyms)
        result = client.create_synonym_map(synonym_map)
        etag = result.e_tag

        synonym_map.synonyms = "\n".join([
            "Washington, Wash. => WA",
        ])

        client.create_or_update_synonym_map(synonym_map)

        result.e_tag = etag
        with pytest.raises(HttpResponseError):
            client.create_or_update_synonym_map(result, match_condition=MatchConditions.IfNotModified)


class SearchSkillsetClientTest(AzureMgmtTestCase):

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_skillset(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))

        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc")

        result = client.create_skillset(skillset)
        assert isinstance(result, SearchIndexerSkillset)
        assert result.name == "test-ss"
        assert result.description == "desc"
        assert result.e_tag
        assert len(result.skills) == 1
        assert isinstance(result.skills[0], EntityRecognitionSkill)

        assert len(client.get_skillsets()) == 1

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_skillset(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc")

        result = client.create_skillset(skillset)
        assert len(client.get_skillsets()) == 1

        client.delete_skillset("test-ss")
        assert len(client.get_skillsets()) == 0

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_skillset_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc")

        result = client.create_skillset(skillset)
        etag = result.e_tag

        skillset = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="updated")
        updated = client.create_or_update_skillset(skillset)
        updated.e_tag = etag

        with pytest.raises(HttpResponseError):
            client.delete_skillset(updated, match_condition=MatchConditions.IfNotModified)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_skillset(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc")
        client.create_skillset(skillset)
        assert len(client.get_skillsets()) == 1

        result = client.get_skillset("test-ss")
        assert isinstance(result, SearchIndexerSkillset)
        assert result.name == "test-ss"
        assert result.description == "desc"
        assert result.e_tag
        assert len(result.skills) == 1
        assert isinstance(result.skills[0], EntityRecognitionSkill)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_skillsets(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset1 = SearchIndexerSkillset(name='test-ss-1', skills=list([s]), description="desc1")
        client.create_skillset(skillset1)
        skillset2 = SearchIndexerSkillset(name='test-ss-2', skills=list([s]), description="desc2")
        client.create_skillset(skillset2)
        result = client.get_skillsets()
        assert isinstance(result, list)
        assert all(isinstance(x, SearchIndexerSkillset) for x in result)
        assert set(x.name for x in result) == {"test-ss-1", "test-ss-2"}

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_skillset(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset1 = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc1")
        client.create_or_update_skillset(skillset1)
        skillset2 = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc2")
        client.create_or_update_skillset(skillset2)
        assert len(client.get_skillsets()) == 1

        result = client.get_skillset("test-ss")
        assert isinstance(result, SearchIndexerSkillset)
        assert result.name == "test-ss"
        assert result.description == "desc2"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_skillset_inplace(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset1 = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc1")
        ss = client.create_or_update_skillset(skillset1)
        skillset2 = SearchIndexerSkillset(name='test-ss', skills=[s], description="desc2", skillset=ss)
        client.create_or_update_skillset(skillset2)
        assert len(client.get_skillsets()) == 1

        result = client.get_skillset("test-ss")
        assert isinstance(result, SearchIndexerSkillset)
        assert result.name == "test-ss"
        assert result.description == "desc2"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_skillset_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        s = EntityRecognitionSkill(inputs=[InputFieldMappingEntry(name="text", source="/document/content")],
                                   outputs=[OutputFieldMappingEntry(name="organizations", target_name="organizations")])

        skillset1 = SearchIndexerSkillset(name='test-ss', skills=list([s]), description="desc1")
        ss = client.create_or_update_skillset(skillset1)
        etag = ss.e_tag
        skillset2 = SearchIndexerSkillset(name='test-ss', skills=[s], description="desc2", skillset=ss)
        client.create_or_update_skillset(skillset2)
        assert len(client.get_skillsets()) == 1

class SearchDataSourcesClientTest(AzureMgmtTestCase):

    def _create_data_source_connection(self, name="sample-datasource"):
        container = SearchIndexerDataContainer(name='searchcontainer')
        data_source_connection = SearchIndexerDataSourceConnection(
            name=name,
            type="azureblob",
            connection_string=CONNECTION_STRING,
            container=container
        )
        return data_source_connection

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_datasource(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        result = client.create_data_source_connection(data_source_connection)
        assert result.name == "sample-datasource"
        assert result.type == "azureblob"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_datasource(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        result = client.create_data_source_connection(data_source_connection)
        assert len(client.get_data_source_connections()) == 1
        client.delete_data_source_connection("sample-datasource")
        assert len(client.get_data_source_connections()) == 0

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_datasource(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        created = client.create_data_source_connection(data_source_connection)
        result = client.get_data_source_connection("sample-datasource")
        assert result.name == "sample-datasource"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_list_datasource(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection1 = self._create_data_source_connection()
        data_source_connection2 = self._create_data_source_connection(name="another-sample")
        created1 = client.create_data_source_connection(data_source_connection1)
        created2 = client.create_data_source_connection(data_source_connection2)
        result = client.get_data_source_connections()
        assert isinstance(result, list)
        assert set(x.name for x in result) == {"sample-datasource", "another-sample"}

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_datasource(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        created = client.create_data_source_connection(data_source_connection)
        assert len(client.get_data_source_connections()) == 1
        data_source_connection.description = "updated"
        client.create_or_update_data_source_connection(data_source_connection)
        assert len(client.get_data_source_connections()) == 1
        result = client.get_data_source_connection("sample-datasource")
        assert result.name == "sample-datasource"
        assert result.description == "updated"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_datasource_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        created = client.create_data_source_connection(data_source_connection)
        etag = created.e_tag

        # Now update the data source connection
        data_source_connection.description = "updated"
        client.create_or_update_data_source_connection(data_source_connection)

        # prepare data source connection
        data_source_connection.e_tag = etag # reset to the original data source connection
        data_source_connection.description = "changed"
        with pytest.raises(HttpResponseError):
            client.create_or_update_data_source_connection(data_source_connection, match_condition=MatchConditions.IfNotModified)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_datasource_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        created = client.create_data_source_connection(data_source_connection)
        etag = created.e_tag

        # Now update the data source connection
        data_source_connection.description = "updated"
        client.create_or_update_data_source_connection(data_source_connection)

        # prepare data source connection
        data_source_connection.e_tag = etag # reset to the original data source connection
        with pytest.raises(HttpResponseError):
            client.delete_data_source_connection(data_source_connection, match_condition=MatchConditions.IfNotModified)
            assert len(client.get_data_source_connections()) == 1

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_datasource_string_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        data_source_connection = self._create_data_source_connection()
        created = client.create_data_source_connection(data_source_connection)
        etag = created.e_tag

        # Now update the data source connection
        data_source_connection.description = "updated"
        client.create_or_update_data_source_connection(data_source_connection)

        # prepare data source connection
        data_source_connection.e_tag = etag # reset to the original data source connection
        with pytest.raises(ValueError):
            client.delete_data_source_connection(data_source_connection.name, match_condition=MatchConditions.IfNotModified)


class SearchIndexersClientTest(AzureMgmtTestCase):

    def _prepare_indexer(self, endpoint, api_key, name="sample-indexer", ds_name="sample-datasource", id_name="hotels"):
        con_str = self.settings.AZURE_STORAGE_CONNECTION_STRING
        self.scrubber.register_name_pair(con_str, 'connection_string')
        container = SearchIndexerDataContainer(name='searchcontainer')
        data_source_connection = SearchIndexerDataSourceConnection(
            name=ds_name,
            type="azureblob",
            connection_string=con_str,
            container=container
        )
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        ds = client.create_data_source_connection(data_source_connection)

        index_name = id_name
        fields = [
        {
          "name": "hotelId",
          "type": "Edm.String",
          "key": True,
          "searchable": False
        }]
        index = SearchIndex(name=index_name, fields=fields)
        ind = SearchIndexClient(endpoint, AzureKeyCredential(api_key)).create_index(index)
        return SearchIndexer(name=name, data_source_name=ds.name, target_index_name=ind.name)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        result = client.create_indexer(indexer)
        assert result.name == "sample-indexer"
        assert result.target_index_name == "hotels"
        assert result.data_source_name == "sample-datasource"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        result = client.create_indexer(indexer)
        assert len(client.get_indexers()) == 1
        client.delete_indexer("sample-indexer")
        assert len(client.get_indexers()) == 0

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_reset_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        result = client.create_indexer(indexer)
        assert len(client.get_indexers()) == 1
        result = client.reset_indexer("sample-indexer")
        assert client.get_indexer_status("sample-indexer").last_result.status in ('InProgress', 'reset')

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_run_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        result = client.create_indexer(indexer)
        assert len(client.get_indexers()) == 1
        start = time.time()
        client.run_indexer("sample-indexer")
        assert client.get_indexer_status("sample-indexer").status == 'running'

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        created = client.create_indexer(indexer)
        result = client.get_indexer("sample-indexer")
        assert result.name == "sample-indexer"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_list_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer1 = self._prepare_indexer(endpoint, api_key)
        indexer2 = self._prepare_indexer(endpoint, api_key, name="another-indexer", ds_name="another-datasource", id_name="another-index")
        created1 = client.create_indexer(indexer1)
        created2 = client.create_indexer(indexer2)
        result = client.get_indexers()
        assert isinstance(result, list)
        assert set(x.name for x in result) == {"sample-indexer", "another-indexer"}

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_indexer(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        created = client.create_indexer(indexer)
        assert len(client.get_indexers()) == 1
        indexer.description = "updated"
        client.create_or_update_indexer(indexer)
        assert len(client.get_indexers()) == 1
        result = client.get_indexer("sample-indexer")
        assert result.name == "sample-indexer"
        assert result.description == "updated"

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_get_indexer_status(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        result = client.create_indexer(indexer)
        status = client.get_indexer_status("sample-indexer")
        assert status.status is not None

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_create_or_update_indexer_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        created = client.create_indexer(indexer)
        etag = created.e_tag


        indexer.description = "updated"
        client.create_or_update_indexer(indexer)

        indexer.e_tag = etag
        with pytest.raises(HttpResponseError):
            client.create_or_update_indexer(indexer, match_condition=MatchConditions.IfNotModified)

    @SearchResourceGroupPreparer(random_name_enabled=True)
    @SearchServicePreparer(schema=SCHEMA, index_batch=BATCH)
    def test_delete_indexer_if_unchanged(self, api_key, endpoint, index_name, **kwargs):
        client = SearchIndexerClient(endpoint, AzureKeyCredential(api_key))
        indexer = self._prepare_indexer(endpoint, api_key)
        result = client.create_indexer(indexer)
        etag = result.e_tag

        indexer.description = "updated"
        client.create_or_update_indexer(indexer)

        indexer.e_tag = etag
        with pytest.raises(HttpResponseError):
            client.delete_indexer(indexer, match_condition=MatchConditions.IfNotModified)
