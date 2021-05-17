let arrayOfProject = [
    'Testing on Production'
];

async function asyncForEach(array, callback) {
    for (let index = 0; index < array.length; index++) {
        await callback(array[index], index, array);
    }
}

submitProjectAsync = async (project) => {
    await $.post('http://105pmasql/pma/project/submitportal/',
        {
            __RequestVerificationToken: '0y75U9iIzyCKIzJlYOG8VuRTmHuCfPYmODNNObUWocBvR3kv3p0ZnhmyQ9i1mmdcdcyZfQIbbyw3QQlci9qXCSiDqcruplEFUHtzJZyQLtMVfqdL1xdJFy5PAm87NHue0',
            IsAutoGenerateProjectNo: true,
            IsShowListPrefix: true,
            PrefixName: 'PMA',
            ProjectName: project,
            ScopeId: 12,
            ServiceTypeId: 'b4d8200c-5566-498b-8d03-a8a70097cd67',
            BranchId: '3d4e34b9-6ace-49dc-a96e-a7eb0071e9f5',
            PriorityId: 'ff688692-5ded-4ca9-83cc-779ebef210b9',
            IsRequestor: true,
            RequestedBy: 862,
            Coordinator: 862,
            TaskDescription: '<div><br></div>'
        }
    )
}

const submitProjectsAsync = async () => {
    await asyncForEach(arrayOfProject, submitProjectAsync);
};

submitProjectsAsync();
