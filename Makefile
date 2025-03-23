default:
	@echo 'Targets:'
	@echo '  garber-visible      -- Observer plan for Garber Nature Center (only visible objects)'
	@echo '  garber-visible-rr   -- Observer plan for Garber Nature Center (only visible objects, with round-robin sorting)'
	@echo '  garber-all          -- Observer plan for Garber Nature Center (all objects)'
	@echo '  help                -- Show help'

garber-visible:
	uv run stellar-plan-cli.py --latitude 39.882859 --longitude -84.549689 --datetime '2025-4-5 21:00:00' --timezone 'America/New_York' --height 390 --visible

garber-visible-rr:
	uv run stellar-plan-cli.py --latitude 39.882859 --longitude -84.549689 --datetime '2025-4-5 21:00:00' --timezone 'America/New_York' --height 390 --visible --roundrobin

garber-all:
	uv run stellar-plan-cli.py --latitude 39.882859 --longitude -84.549689 --datetime '2025-4-5 21:00:00' --timezone 'America/New_York' --height 390

help:
	uv run stellar-plan-cli.py --help
