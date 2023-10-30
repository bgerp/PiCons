За Windows трябва да се добавят 2 задачи в task_scheduler-a за да поправят настройките на COM порта при стартиране на компютъра и при хибернизация.
- стартира се `powershell c:\пълен път до\comport_elicom.ps1` в задачa с два тригера:
1. `At log on`
2. `On an event` - `System / Kernel Power / 107 as an event trigger` за възстановяване след хибернация
3. Командата `c:\PHP\php -S localhost:80 -t c:\пълен път до\PiCons\` трябва да е на тригер - `at startup`
