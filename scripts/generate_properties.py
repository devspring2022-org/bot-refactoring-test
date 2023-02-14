reduced_keys = ['id', 'node_id', 'url', 'actor', 'event', 'commit_id', 'commit_url', 'created_at', 'label', 'performed_via_github_app']
with open("sample.txt", "a") as file_object:
    for key in reduced_keys:
        file_object.write(f'        self.{key} = self._data["{key}"]\n')