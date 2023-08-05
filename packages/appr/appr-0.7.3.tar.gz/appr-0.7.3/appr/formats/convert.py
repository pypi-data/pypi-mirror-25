
    def create_kub_resources(self, resources):
        r = []
        for resource in resources:
            name = resource['metadata']['name']
            kind = resource['kind'].lower()
            protected = resource.get('annotations', {}).get(ANNOTATIONS['protected'], False)
            r.append({
                "file": "%s-%s.yaml" % (name, kind),
                "name": name,
                "generated": True,
                "order": -1,
                "protected": protected,
                "value": resource,
                "patch": [],
                "variables": {},
                "type": kind})
        return r
