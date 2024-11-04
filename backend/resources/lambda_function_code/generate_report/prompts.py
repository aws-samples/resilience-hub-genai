from string import Template



def executive(report: str) -> str:
    prompt_template = Template("""
    # AWS Resilience Hub resiliency assessments
    {{$report}}
                               
    # Instructions                           
    Report for a CIO.
    The CIO is interested in a high-level overview of the organization's overall resilience posture, including:
    - Executive summary of the assessment results
    - Identification of critical risks and vulnerabilities
    - Cost implications and potential return on investment (ROI) for recommended resilience improvements
    
    # Output
    Return the report as HTML <HTML></HTML>
    """)
    prompt = prompt_template.substitute(report=report)
    return trim(prompt)


def manager(report: str) -> str:
    prompt_template = Template("""
    # AWS Resilience Hub resiliency assessments
    {{$report}}
                               
    # Instructions                           
    Report for a Director of Infrastructure.
    The Director of Infrastructure is interested in the technical details and operational aspects of the assessment, such as:    
    - Detailed assessment of the infrastructure components (e.g., networks, servers, storage, databases)
    - Identification of single points of failure and potential bottlenecks
    - Evaluation of disaster recovery and business continuity plans
    - Recommendations for improving infrastructure resilience (e.g., redundancy, failover mechanisms, capacity planning)
    - Impact analysis of potential disruptions and outages on infrastructure components
    
    # Output
    Return the report as HTML <HTML></HTML>
    """)
    prompt = prompt_template.substitute(report=report)
    return trim(prompt)


def engineer(report: str) -> str:
    prompt_template = Template("""
    # AWS Resilience Hub resiliency assessments
    {{$report}}
                               
    # Instructions
    Report for SRE or Developer.
    SREs and developers are interested in the aspects related to application resilience and operational practices, including:
    - Group Logical ID's together by recommendations and make the most concise report possible.

    # Output
    Return the report as HTML <HTML></HTML>
    """)
    prompt = prompt_template.substitute(report=report)
    return trim(prompt)


def trim(text: str) -> str:
    return text.replace('\n    ','\n')
