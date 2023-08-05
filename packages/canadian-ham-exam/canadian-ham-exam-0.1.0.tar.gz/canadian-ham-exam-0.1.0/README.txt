# Canadian HAM Exam

Canadian Ham Exam uses the official question bank from Industry Canada and
allows aspiring hams to practice the section of their choice as they are
learning the material for the exam.

It requires a copy of the question bank, which can be downloaded free of
charge from the Industry Canada website:

  http://www.ic.gc.ca/eic/site/025.nsf/eng/h_00004.html

## Installation

To install using pip, simply do this:

    $ pip install canadian-ham-exam

## Usage

The most basic way to start a quiz is to run the command by specifying the
path to the Industry Canada question bank:

    canadian-ham-exam amat_basic_quest_delim.txt

If you'd like to restrict the quiz to specific sections of the question
bank, you can do so with the `--sections` (or `-s` for short) option:

    canadian-ham-exam --sections 1-4 amat_basic_quest_delim.txt
    canadian-ham-exam -s 3,5,6 amat_basic_quest_delim.txt

You can specify the number of questions you'd like to answer (the default is
100) using the `--number` parameter:


    canadian-ham-exam -n 25 amat_basic_quest_delim.txt

You can see the full list of command-line options by running:

    canadian-ham-exam --help

## License

Copyright (C) 2017  Francois Marier <francois@fmarier.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
