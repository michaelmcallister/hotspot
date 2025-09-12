SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:

DB      := hotspot.db
SCHEMA  := create_tables.txt
CSVS    := default_risk.csv model_risk.csv postcode_risk.csv

# This is a hack (or really clever?) but uses the file name of the csvs as the table name 
define IMPORT_LINE
.import --csv --skip 1 '$(1)' $(basename $(notdir $(1)))
endef
IMPORTS := $(foreach f,$(CSVS),$(call IMPORT_LINE,$(f)))

.PHONY: all rebuild clean
all: $(DB)

$(DB): $(SCHEMA) $(CSVS)
	@set -euo pipefail; \
	tmp="$(DB).tmp"; \
	rm -f "$$tmp"; \
	{ \
		echo ".read $(SCHEMA)"; \
		echo ".mode csv"; \
		echo ".separator ,"; \
		$(foreach f,$(CSVS),echo ".import --csv --skip 1 '$(f)' $(basename $(notdir $(f)))";) \
	} | sqlite3 -batch "$$tmp"; \
	mv "$$tmp" "$(DB)"; \
	echo Done.

rebuild: clean all

clean:
	rm -f "$(DB)"

