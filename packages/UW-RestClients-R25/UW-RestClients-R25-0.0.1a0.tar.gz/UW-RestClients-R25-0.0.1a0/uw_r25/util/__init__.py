from restclients_core.util.decorators import use_mock
from uw_r25.dao import R25_DAO

fdao_r25_override = use_mock(R25_DAO())
