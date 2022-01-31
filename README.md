<p align="center">
  <i><span style="font-size: small;">
  	Systems and Methods for Big and Unstructured Data - Delivery #3 - AA 2021/2022 - Prof. Marco Brambilla
  </span></i>
</p>
<h1 align="center">
	<strong>
	ELK Vaccination Campaign Analysis System
	</strong>
	<br>
</h1>
<p align="center">
<span style="font-size: small; ">
		<a href="https://www.mongodb.com">MongoDB</a>		 
		•		
		<a href="Report.pdf">Report</a>   
	</span>
</p>

Considering the scenario in which there’s the need to build a system suitable for analysis over 
data about COVID-19 vaccination statistics, we designed and build a Kibana visualization 
tool relying on the ELK stack. The data stored allows extracting actionable insights 
concerning various statistical purposes, involving information such as vaccine deliveries, 
administered doses amounts, suppliers and age groups. 
The third-part data imported into the database is updated daily as it concerns vaccination campaign 
and so it has been also used to build insightful dashboards providing visualization at various levels 
of granularity.


# Contents

- ⚙  [System requirements️](#system-requirements)
- 🚀 [Setup instructions](#-setup-instructions)
- 📜 [Report](Report.pdf)
- 👨‍💻 [Usage](#-usage)
- 🗄️ Dumps
  - 🗄️ [Dashboards dump](Exports/Dashboards)
  - 🗄️ [ES Indexes dump](Exports/Indexes)  
- 📷 [Screenshots](#-screenshots)  
- 📝 [License](#-license)

# System requirements

## Required software

- [Python](https://www.python.org/) 3.8 or higher
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Kibana](https://www.elastic.co/kibana/)  
- Python modules in [requirements.txt](requirements.txt)


# 🚀 Setup instructions

## Clone the repo

    git clone https://github.com/pablogiaccaglia/elastichsearch-vaccination-campaign
    cd elasticsearch_smbud/

## Install required packages

From the project's directory run the following commands:

    pip install -r requirements.txt
    
# 👨‍💻 Usage

# 📷 Dashboards


Weekly trend of the number of vaccinations       |  Vaccination status of all age groups
:-------------------------:|:-------------------------:
![](report/latex/Weekly%20trend%20of%20the%20number%20of%20vaccinations.png)|  ![](report/latex/Vaccination%20status%20of%20all%20age%20groups.png)

---

Total number of doses delivered      |  Number of not vaccinated people
:-------------------------:|:-------------------------:
![](report/latex/Total%20number%20of%20doses%20delivered.png)|  ![](report/latex/Number%20of%20not%20vaccinated%20people.png)

---

Gender distribution of weekly vaccine doses administered           |  Doses map
:-------------------------:|:-------------------------:
![](report/latex/Gender%20distribution%20of%20weekly%20vaccine%20doses%20administered.png)|  ![](report/latex/Doses_map.png)

---

<h3><p align="center"><b>Distribution of suppliers of all administered vaccines</b></></h3> 
	
<p align="center">
<img src="https://github.com/pablogiaccaglia/elk-vaccination-analysis/blob/master/report/latex/Distribution%20of%20suppliers%20of%20all%20administered%20vaccines.png" width=550px height=520px/>
</p>

# 📝 License

This file is part of "ELK Vaccination Campaign Analysis System".

"ELK Vaccination Campaign Analysis System" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"ELK Vaccination Campaign Analysis System" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program (LICENSE.txt).  If not, see <http://www.gnu.org/licenses/>
