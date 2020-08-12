/*******************************************************************************
 * Copyright 2017 Cognizant Technology Solutions
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy
 * of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 ******************************************************************************/
package com.cognizant.devops.platformreports.assessment.datamodel;

import java.util.HashMap;
import java.util.Map;

import com.google.gson.JsonArray;

public class InsightsAssessmentConfigurationDTO {
	
	private int reportId;
	private int configId;
	private String asseementreportname;
	private String reportName;
	private String reportFilePath;
	private long executionId;
	private String workflowId;
	private String pdfReportDirPath;
	private String pdfReportFolderName;
	Map<String, JsonArray> contentJsonObjMap = new HashMap<>();
	Map<String, JsonArray> tableJsonObjMap = new HashMap<>();
	JsonArray visualizationResult = new JsonArray();

	public int getReportId() {
		return reportId;
	}

	public void setReportId(int reportId) {
		this.reportId = reportId;
	}

	public String getAsseementreportname() {
		return asseementreportname;
	}
	public void setAsseementreportname(String asseementreportname) {
		this.asseementreportname = asseementreportname;
	}

	public String getReportName() {
		return reportName;
	}

	public void setReportName(String reportName) {
		this.reportName = reportName;
	}

	public String getReportFilePath() {
		return reportFilePath;
	}

	public void setReportFilePath(String reportFilePath) {
		this.reportFilePath = reportFilePath;
	}

	public int getConfigId() {
		return configId;
	}

	public void setConfigId(int configId) {
		this.configId = configId;
	}

	public long getExecutionId() {
		return executionId;
	}

	public void setExecutionId(long executionId) {
		this.executionId = executionId;
	}

	public String getWorkflowId() {
		return workflowId;
	}

	public void setWorkflowId(String workflowId) {
		this.workflowId = workflowId;
	}

	public String getPdfReportDirPath() {
		return pdfReportDirPath;
	}

	public void setPdfReportDirPath(String pdfReportDirPath) {
		this.pdfReportDirPath = pdfReportDirPath;
	}

	public String getPdfReportFolderName() {
		return pdfReportFolderName;
	}

	public void setPdfReportFolderName(String pdfReportFolderName) {
		this.pdfReportFolderName = pdfReportFolderName;
	}

	public Map<String, JsonArray> getContentJsonObjMap() {
		return contentJsonObjMap;
	}

	public void setContentJsonObjMap(Map<String, JsonArray> contentJsonObjMap) {
		this.contentJsonObjMap = contentJsonObjMap;
	}

	public Map<String, JsonArray> getTableJsonObjMap() {
		return tableJsonObjMap;
	}

	public void setTableJsonObjMap(Map<String, JsonArray> tableJsonObjMap) {
		this.tableJsonObjMap = tableJsonObjMap;
	}

	public JsonArray getVisualizationResult() {
		return visualizationResult;
	}

	public void setVisualizationResult(JsonArray visualizationResult) {
		this.visualizationResult = visualizationResult;
	}

	@Override
	public String toString() {
		return "InsightsAssessmentConfigurationDTO [reportId=" + reportId + ", configId=" + configId
				+ ", asseementreportname=" + asseementreportname + ", reportName=" + reportName + ", reportFilePath="
				+ reportFilePath + ", executionId=" + executionId + ", workflowId=" + workflowId + ", pdfReportDirPath="
				+ pdfReportDirPath + ", pdfReportFolderName=" + pdfReportFolderName + ", contentJsonObjMap="
				+ contentJsonObjMap + ", tableJsonObjMap=" + tableJsonObjMap + "]";
	}
}
